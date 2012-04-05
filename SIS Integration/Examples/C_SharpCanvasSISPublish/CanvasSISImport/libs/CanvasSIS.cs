using System;
using System.Net;
using System.IO;
using System.Collections;
using Procurios.Public;
using System.Collections.Specialized;
using System.Text;

namespace canvasSIS
{
	public class CanvasSIS
	{
		static private string account_id = "2314";
		static private string sub_domain = "canvas";
		static private string access_token = "lkJOIJ2OIJASDFASldkjf";
		public CanvasSIS ()
		{
			
		}
		
		
		public static Hashtable PostCanvasSISImport(string filename, string extension){
			string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/"+account_id+"/sis_imports.json";
			
			NameValueCollection nvc = new NameValueCollection();
			
			nvc.Add("import_type","instructure_csv");
			nvc.Add("access_token",access_token);
			nvc.Add("extension",extension);
			
          WebClient client = new WebClient(); 
			client.QueryString = nvc;
			
			client.Headers.Add("Content-Type","application/x-www-form-urlencoded");
			
			byte[] fileContents = System.IO.File.ReadAllBytes(filename);
			
			byte[] responseBinary = client.UploadData(url,"POST",fileContents);
			
			string response = Encoding.UTF8.GetString(responseBinary);	
			
			
			Console.WriteLine("response: " + response);
			// return response;
			Hashtable json_response = returnJson(response);
			json_response["raw_response"] = response;
			return json_response;
		}
		public static Hashtable PostCanvasSISImport(string filename)
		{
			 return PostCanvasSISImport(filename,"csv");
		}
		
		public static Hashtable CheckStatus(String sis_import_id)
		{
			//string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/82726/sis_imports/"+sis_import_id +".json?access_token=h3xyPlREWirj4FDjJTzlpAWPakHgVzCx0nJlwYA4XcX2tvqa6j6YEBo7AoOfvSQW";
            string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/"+account_id+"/sis_imports/"+sis_import_id+".json?access_token="+access_token;
           	
           	NameValueCollection nvc = new NameValueCollection();
			
			nvc.Add("access_token",access_token);
			WebClient client = new WebClient(); 
			client.QueryString = nvc;
			byte[] responseBinary = client.DownloadData(url);
			string response = Encoding.UTF8.GetString(responseBinary);
			
			//return response;
			Hashtable json_response = returnJson(response);
			json_response["raw_response"] = response;
			return json_response;
			
		}
		public static Hashtable returnJson(string s){
			Hashtable o;
			//bool success = true;
			o = (Hashtable)JSON.JsonDecode(s);	
			//Console.WriteLine (o["id"]);
			return o;
		}
	}
}

