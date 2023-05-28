#! /usr/bin/ruby

require "openai"
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: shiritori-AI.rb [options]"

  opts.on('-d', '--[no-]debug', 'Run in Debug mode')  { |v| options[:debug] = v }
  opts.on('-l', '--local',      'Not access ChatGPT') { |v| options[:local] = v }
end.parse!

access_token = open('open-ai.key').read.to_s

class Conversation < Array
  def initialize
    @initial_word = 'しりとり'
    @first_system_prompt = open('first_system_prompt.txt').read.gsub(/\s+/, '')

    self << { role: 'system', content: @first_system_prompt.gsub(/\n/, ''), valid?: nil  }
    self << { role: 'user',   content: @initial_word,                       valid?: true }
  end

  def messages
    self.map { |message| message.dup.delete_if { |k, v| k == :valid? } }
  end

  def add(word)
    if word.match(/「/)
      word = GPTResponse::sanitise(word)
    end

    if word.ends_with_nn?
      last_valid_word = select { |message| message[:valid?] }.last[:content]
      prompt = '単語が「ん」で終わっています。「' + last_valid_word.split(//).last + '」で始まる別の単語で答えて下さい。'
      puts 'SYSTEM: ' + prompt

      add_invalid(word)
      add_system_prompt(prompt)
    elsif word.includes_other_than_kana?
      prompt = 'かな文字以外が使われています。ひらがな又はカタカナだけで答えて下さい。'
      puts 'SYSTEM: ' + prompt

      add_invalid(word)
      add_system_prompt(prompt)
    else
      add_valid(word)
    end
  end

  private

  def add_valid(word)
    swap_user_assistant_roles_if_valid
    self << { role: 'user', content: word, valid?: true }
  end

  def add_invalid(word)
    self << { role: 'assistant', content: word, valid?: false }
  end

  def add_system_prompt(prompt)
    self << { role: 'system', content: prompt, valid?: nil }
  end

  def swap_user_assistant_roles_if_valid
    self.each do |message|
      next if message[:role] == 'system'
      next if message[:valid?] == false

      if message[:role] == 'user'
        message[:role] = 'assistant'
      else
        message[:role] = 'user'
      end
    end
  end
end

class String
  def ends_with_nn?
    split(//).last == 'ん'
  end

  def includes_other_than_kana?
    ! match(/^[\p{Hiragana}|\p{Katakana}]+$/)
  end
end

class GPTResponse
  def self.sanitise(string)
    ret = string.sub(/.*「/, '').sub(/」.*/, '')
  end
end

client = OpenAI::Client.new(access_token: access_token)
conversation = Conversation.new
local_words = open('local_words.txt').to_a.map { |word| word.sub(/\s+/, '') }
log = open('shiritori-AI.log', 'w')

while true do
  if options[:debug]
    depth = 3
    p conversation.slice(conversation.size - depth, depth)
  end

  unless options[:local]
    response = client.chat(parameters: { model: "gpt-3.5-turbo", messages: conversation.messages, })
    if response.dig('error', 'type') == 'server_error'
      sleep 20
      redo
    end
  end
  log.print conversation.pretty_inspect
  log.print "\n\n"

  if options[:local]
    word = local_words.shift
  else
    word = response.dig('choices', 0, 'message', 'content')
  end
  puts word

  conversation.add(word)

  sleep 21 unless options[:local]
end
