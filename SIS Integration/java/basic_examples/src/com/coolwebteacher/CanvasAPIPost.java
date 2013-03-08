package com.coolwebteacher;

import com.coolwebteacher.canvasapi.ImportSIS;

public class CanvasAPIPost {

	
	public static void main(String[] args) {

		ImportSIS importer = new ImportSIS();
		
		// Figure out what folder this file is running in.
		String path = System.getProperty("user.dir");
		String config_path = path + "/config.json";
		// Load the config file (JSON) from the local director
		importer.readConfigFromFile(config_path);
	
		importer.log("Config file has been read, now importing");
		
		// Send the import
		int sis_import_id = importer.doImport();
		
		importer.log("File uploaded, id: " + sis_import_id);
		
		// Wait for the import to complete and save the response
		String completion = importer.WaitForCompletion(sis_import_id,10);
		
		importer.log(completion);

	}

}
