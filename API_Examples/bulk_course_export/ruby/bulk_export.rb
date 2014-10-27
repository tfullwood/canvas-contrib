# Edit these:
access_token = "4344~PzZ13RQj9GIZnBSQFPkgswwyvQM31DxcYICihbcLg7O3gZj9nAaXgMJeFVewV2QM"# nil
domain = "bbroderick" #nil
env = nil
input_file = "./in.csv" #nil
output_file = "./out.csv" #nil
#============
# Don't edit from here down unless you know what you're doing.

require 'unirest'
require 'csv'

unless access_token
  "Puts what is your access token?"
  access_token = gets.chomp
end

unless domain
  "Puts what is your Canvas domain?"
  domain = gets.chomp
end

unless input_file
  "Puts where is your input CSV, listing courses to migrate, located?"
  input_file = gets.chomp
end

unless output_file
  "Puts where would you like to output your CSV to?"
  output_file = gets.chomp
end

unless File.exists?(input_file)
  raise "Error: can't locate the input CSV"
end

unless File.exists?(output_file)
  CSV.open(output_file, 'wb') do |csv|
    csv << ["course_id", "export_url"]
  end
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

CSV.foreach(input_file, {:headers => true}) do |cid|
  url ="#{base_url}/courses/#{cid[0]}/content_exports"
  export_course = Unirest.post(url, parameters: { "export_type" => "common_cartridge", "skip_notifications" => 1 })
  job = export_course.body

  while job["workflow_state"] == "created" || job["work_flow_state"] == "importing"
    puts "importing"
    sleep(3)
    export_status = Unirest.get("#{url}/#{job['id']}")
    job = export_status.body
  end
    
  if job["processing_errors"]
    puts "An error occurred exporting this job. \n #{job}"
  end

  if job["processing_warnings"]
    puts "Processing Warning: #{job["processing_errors"]}"
  end

  CSV.open(output_file, 'ab') do |csv|
    csv << ["#{job['course_id']}", "#{job['attachment']['url']}"]
  end
end

puts "Successfully exported files."
