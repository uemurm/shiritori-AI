#! /usr/bin/ruby

require "openai"
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: shiritori-AI.rb [options]"

  opts.on('-d', '--[no-]debug', 'Run in Debug mode')  { |v| options[:debug] = v }
  opts.on('-l', '--local',      'Not access ChatGPT') { |v| options[:local] = v }
end.parse!

# todo: Create a file 'open-ai.key' then read it instead.
access_token = ENV['OPENAI_API_KEY']

class Conversation < Array
  def initialize
    @initial_word = 'しりとり'
    # todo: Create a file 'system_prompt.txt'
    @system_prompt = <<-EOS
私は日本語を勉強しています。
あなたには、しりとりの相手役をお願いします。
しりとりの答えだけを、単語ひとつで答えて下さい。
ひらがなだけで答えて下さい。
一般名詞で答えて下さい。
「ん」以外で終わる単語で答えて下さい。
「ん」で終わる単語は使わないで下さい。
    EOS

    self << { role: 'system', content: @system_prompt.gsub(/\n/, ''), valid?: true }
    self << { role: 'user', content: @initial_word, valid?: true }
  end

  def messages
    self.map { |message| message.dup.delete_if { |k, v| k == :valid? } }
  end

  def add(word)
    if word.match(/「/)
      word = GPTResponse::sanitise(word)
    end

    if word.ends_with_nn?
      previous_word = select { |message| message[:role] != 'system' }.last[:content]
      prompt = '単語が「ん」で終わっています。「' + previous_word.split(//).last + '」で始まる別の単語で答えて下さい。'
      puts 'SYSTEM: ' + prompt

      add_invalid(word)
      add_system_prompt(prompt)
      # puts 'You lose!'
      # break
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
    self << { role: 'system', content: prompt, valid?: true }
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

File.open('gpt.log', "w") do |f|
  while true do
    if options[:debug]
      depth = 3
      p conversation.slice(conversation.size - depth, depth)
    end

    unless options[:local]
      while (response = client.chat(parameters: { model: "gpt-3.5-turbo", messages: conversation.messages, });
        response.dig('error', 'type') == 'server_error'
        ) do
          sleep 20
      end
    end
    f.print conversation.pretty_inspect
    f.print "\n\n"

    if options[:local]
      word = local_words.shift
    else
      word = response.dig('choices', 0, 'message', 'content')
    end
    puts word

    conversation.add(word)

    sleep 21 unless options[:local]
  end
end
