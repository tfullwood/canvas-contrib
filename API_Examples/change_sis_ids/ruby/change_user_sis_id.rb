require 'unirest'
require 'csv'

#================
# Change these
access_token = nil
domain = nil
env = nil
csv_file = nil

#================
# Don't edit from here down unless you know what you're doing.

unless access_token
  "Puts what is your access token?"
  access_token = gets.chomp
end

unless domain
  "Puts what is your Canvas domain?"
  domain = gets.chomp
end

unless csv_file
  "Puts where is your SIS ID update CSV located?"
  csv_file = gets.chomp
end

unless File.exists?(csv_file)
  raise "Error: can't locate the update CSV"
end

env ? env << "." : env
base_url = "https://#{domain}.#{env}instructure.com/api/v1"
test_url = "#{base_url}/accounts/self"

Unirest.default_header("Authorization", "Bearer #{access_token}")

# Make generic API call to test token, domain, and env.
test = Unirest.get(test_url)

unless test.code == 200
  raise "Error: The token, domain, or env variables are not set correctly"
end

CSV.foreach(csv_file, {:headers => true}) do |row|
  url = "#{base_url}/users/sis_user_id:#{row[0]}/logins"
  login_response = Unirest.get(url)
  logins = login_response.body

  unless logins
    puts "User #{row[0]} wasn't found."
    next
  end

  logins.each do |login|
    hashed = login.to_h
    puts hashed['id']
    puts row[0]
    if hashed['sis_user_id'] == row[0]
      update_id = Unirest.put("#{base_url}/accounts/self/logins/#{hashed['id']}", parameters: { 'login[sis_user_id]' => row[1] })
      puts "Successfully updated \n #{update_id.body}"
    else
      puts "User #{row[0]} wasn't found... Moving right along."
    end
  end
end

puts "Finished updating user SIS IDs."
