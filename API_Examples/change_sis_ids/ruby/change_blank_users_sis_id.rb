require 'typhoeus'
require 'csv'

#================
# Need to have 'canvas_id' & 'new_sis_id' as the column headers.
# canvas_id is the ID Canvas gives the users (Provisioning report)
# new_sis_id is the value you want to give the user.
# Change these
access_token = nil
domain = nil
env = nil
csv_file = nil
#
##================
## Don't edit from here down unless you know what you're doing.
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

headers = { "Authorization" => "Bearer #{access_token}" }
counter = 0
hydra = Typhoeus::Hydra.new(max_concurrency: 20)

# Make generic API call to test token, domain, and env.
test = Typhoeus::Request.new(test_url, headers: headers)
test.run

unless test.response.code == 200
	puts test.response.code
	puts test.response.body
	raise "Error: The token, domain, or env variables are not set correctly"
end

CSV.foreach(csv_file, {:headers => true}) do |row|
	if row.headers[0] != 'canvas_id' || row.headers[1] != 'new_sis_id'
		raise "CSV headers need to be 'canvas_id' for the ID Canvas uses, & 'new_user_id' for the SIS ID value you want to give the users."
	else	
	csv_id = row['canvas_id']
	url = "#{base_url}/users/#{csv_id}/logins"
	#	puts url
	login_request = Typhoeus::Request.new(url, headers: headers)
	login_request.run
	logins = JSON.parse(login_request.response.body)
	# test if this is specific enough. Seems like it needs to be more specific, cause error messages should fail it.

	unless logins
		puts "User #{csv_id} wasn't found."
		next
	end

	#	puts logins
	#	puts logins.class

	logins.each do |login|
		hashed = login.to_h
		#	puts hashed['user_id']
		#	puts csv_id
		if hashed['user_id'].to_s == csv_id
			update_id = Typhoeus::Request.new("#{base_url}/accounts/self/logins/#{hashed['id']}", params: { 'login[sis_user_id]' => row['new_sis_id'] }, headers: headers, method: :put)
			update_id.on_complete do |response|
				if response.code != 200
					puts "HTTP Status: #{response.code} \nError updating SIS for user #{csv_id} \nError: #{response.body} \n"
				else
					puts "Successfully updated #{csv_id} \n#{update_id.response.body}"
				end
			end
			hydra.queue(update_id)

		else
			puts "User #{csv_id} wasn't found... Moving right along."
		end
	end
end
end
hydra.run

puts "Finished updating user SIS IDs."
