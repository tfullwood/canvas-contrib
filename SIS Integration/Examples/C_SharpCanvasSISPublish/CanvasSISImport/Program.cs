using System;
using System.Collections;
using canvasSIS;
using System.Threading;

namespace CanvasSISApplication
{
    class Program
    {
        static void Main(string[] args)
        {
            Hashtable post_results = CanvasSIS.PostCanvasSISImport(@"sis_folders/courses.csv","csv");

            //Console.WriteLine(post_results.Keys.ToString());
            Console.WriteLine("id: " + post_results["id"]);

            // sis_import_id will represent the id of the queued sis import.  It is used
            // later to check the status of the sis import
            string sis_import_id = post_results["id"].ToString();


            Hashtable status;

            do
            {
                status = CanvasSIS.CheckStatus(sis_import_id);

                // Uncomment the next line to see the raw api response output on the console.
                //Console.WriteLine(status["raw_response"]);
                //status = CanvasSIS.returnJson (status_str);
                Console.WriteLine("status: " + status["workflow_state"]);
                //loop_limit--;
                Thread.Sleep(2000);

            } while ((string)status["workflow_state"] == "created");

            Console.WriteLine("status: " + status["workflow_state"]);


        }
    }
}
