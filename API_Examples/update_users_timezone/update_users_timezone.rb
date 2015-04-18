require 'typhoeus'
require 'csv'

access_token = '' 
domain = '' 
url = "https://#{domain}.test.instructure.com/api/v1/"
csv_path = '' 
time_zone = "America/New_York"
########################### DO NOT EDIT ##############################
hydra = Typhoeus::Hydra.new(max_concurrency: 10)

CSV.foreach(csv_path, {:headers => true}) do |row|

	put_response = Typhoeus::Request.new("#{url}users/sis_user_id:#{row[0]}",
		method: :put,
		params: { 'user[time_zone]' => row[1] },
		headers: { 'Authorization' => "Bearer #{access_token}" }
		)

	put_response.on_complete do |response|
		if response.code == 200
			puts "Updated user #{row[0]} with new time zone settings."
		elsif response.code != 200
			puts response.body
		else
			puts "Unable to update user #{row[0]}'s time zone value."
		end
	end
	hydra.queue(put_response)
end

hydra.run
puts 'Completely Done.'
