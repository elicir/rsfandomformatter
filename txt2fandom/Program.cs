using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using Codeplex.Data;


namespace t2f
{
    class Program
    {
        #region Private Properties
        private static readonly HttpClient client = new HttpClient();
        #endregion

        #region API Methods
        private static async Task<DynamicJson> GetJson(string url)
        {
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
            client.DefaultRequestHeaders.Add("User-Agent", ".NET Foundation Repository Reporter");

            var stringTask = client.GetStringAsync(url);
            var json = await stringTask;
            return DynamicJson.Parse(json);
        }


        private static async Task<DynamicJson> GetStory(string code)
        {
            var json = await GetJson("https://karth.top/api/adventure/ww/" + code + ".json");
            return json;
        }

        private static async Task<DynamicJson> GetCharaNames()
        {
            var json = await GetJson("https://karth.top/api/adventure_chara_name.json");
            return json;
        }

        private static async Task<DynamicJson> GetDress(string code)
        {
            var json = await GetJson("https://karth.top/api/dress/" + code + ".json");
            return json;
        }
        #endregion

        #region Helper Methods
        static string Prompt(string message)
        {
            Console.WriteLine(message);
            return Console.ReadLine();
        }

        private static async void ProcessScript(dynamic story, dynamic charaNames)
        {
            foreach (KeyValuePair<string, dynamic> item in story)
            {
                Console.WriteLine(item.Key + ":" + item.Value); // foo:json, bar:100
            }
        }

        #endregion
        static async Task Main(string[] args)
        {
            string code = args[0];
            var story = await GetStory(code);
            var charaNames = await GetCharaNames();
            ProcessScript(story, charaNames);
        }




            static async Task Mai3n(string[] args)
        {
            string code = null;
            string fn;
            string mode;
            string quote = null;
            string character = null;
            bool isArcanaB = false;
            bool isTranscriptOnly = false;
            string[] schools = null;

            if (args.Length == 0)
            {
                // if no args provided, get them from input
                code = Prompt("Enter adventure code: ");
                fn = Prompt("Enter txt file name: ");
                mode = Prompt("Enter story mode (b for bond story: Chapter, e for events: Part, m for main story: Part) ");
                isTranscriptOnly = Prompt("Transcript only? (y/n) ") == "y";
                if (!isTranscriptOnly)
                {
                    isArcanaB = Prompt("Is Arcana bond story? (y/n) ") == "y";
                    if (mode == "b" || isArcanaB)
                    {
                        quote = Prompt("Enter quote (press enter to skip): ");
                        if (quote != "")
                        {
                            character = Prompt("Enter character: ");
                        }
                    }
                    if (mode == "e")
                    {
                        string schoolStr = Prompt("Enter schools for event, separated by comma: ");
                        schools = schoolStr.Split(",");
                    }
                }
            } //TODO: account for quote, character, arcana bond story (default false), transcriptonly (default false), school for event story in one line command line usage
            else if (args.Length == 1)
            {
                fn = "temp.txt";
                if (args[0].Length < 2)
                {
                    Console.WriteLine("You messed something up. Entering prompt mode");
                    fn = Prompt("Enter txt file name: ");
                    mode = Prompt("Enter story mode (b for bond story: Chapter, e for events: Part)");
                }
                else
                {
                    mode = "" + args[0][1];
                }
            }
            else if (args.Length == 2)
            {
                fn = args[0];
                if (args[1].Length < 2) 
                {
                    Console.WriteLine("You messed something up. Entering prompt mode");
                    fn = Prompt("Enter txt file name: ");
                    mode = Prompt("Enter story mode (b for bond story: Chapter, e for events: Part)");
                }
                else
                {
                    mode = "" + args[1][1];
                }
            }
            else
            {
                Console.WriteLine("You messed something up. Entering prompt mode");
                fn = Prompt("Enter txt file name: ");
                mode = Prompt("Enter story mode (b for bond story: Chapter, e for events: Part)");
            }
            

            // init constants
            string chartalk1 = "{{CharTalk|";
            string endCurlyBraces = "}}";
            string new_part = "|-|\n";
            string title1 = mode == "b" ? "Chapter " : "Part ";
            string title1final = "Final Part";
            string title2 = "=\n<span style=\"font-weight: bold; font-size: 20px;\" >";
            string title_end = "</span>";
            string subtitle1 = "<br><span style=\"font-weight: bold; font-size: 16px;\" >";
            string quoteHead = "{{Quote|";
            string category = "[[Category:";
            string endSquareBraces = "]]";
            string tabber1 = "<tabber>";
            string tabber2 = "</tabber>";
            string bondStories = "Bond Stories";
            string mainStories = "Main Stories";
            string eventStories = "Event Stories";
            string stories = "Stories";
            string transcripts = "Transcripts";
            string arcana = "''(Part 1 and Part 2 of [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Third Part: Arcana Arcadia|Arcana Arcadia]] Stage Girl bond stories are viewable in the Gallery under [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Intermission|Arcana Arcadia - Intermission]].)''";

            // create/overwrite transcript.txt to empty
            System.IO.File.Create("transcript.txt").Close();

            using var outfile = System.IO.File.AppendText("transcript.txt");

            if (quote != null)
            {
                outfile.WriteLine(quoteHead + quote + endCurlyBraces);
                if (isArcanaB) outfile.WriteLine(arcana);
            }
            if (!isTranscriptOnly) outfile.WriteLine(tabber1);
            string line = null;
            string newstr;
            // Read the file line by line
            var story = await GetStory(code);
            var charaNames = await GetCharaNames();
            while (line != null)
            {
                if (line[0] == '|')
                {
                    char num = line[1];
                    if (num == 'F' && line[2] == ' ')
                    {
                        newstr = new_part + title1final + title2 + line[3..] + title_end;
                    }
                    else if (int.TryParse(num.ToString(), out _))
                    {
                        newstr = new_part + title1 + num + title2 + line[3..] + title_end;
                    }
                    else 
                    {
                        newstr = new_part + line[1..] + "=";
                    }
                }
                else if (line[0] == '>')
                {
                    if (line[1] == '|')
                    {
                        newstr = subtitle1[4..] + line[2..] + title_end;
                    }
                    else if (line[1] == '.')
                    {
                        newstr = "<hr>";
                    }
                    else
                    {
                        newstr = subtitle1 + line[1..] + title_end;
                    }
                }
                else if (line[0] == '<')
                {
                    newstr = chartalk1 + "|" + line[1..] + endCurlyBraces;
                }
                else
                {
                    int i = line.IndexOf('\\');
                    if (i == -1)
                    {
                        Console.WriteLine("Line missing speaker: " + line);
                        Environment.Exit(1);
                    }
                    string name = line[..i];
                    string speech = line[(i + 1)..];
                    int b = name.IndexOf('(');
                    if (b != -1) 
                    {
                        speech = "'''(" + name[(b + 1)..] + "'''<br>" + speech;
                        name = name[..(b - 1)];
                    }
                    if (name == "Mei Fan")
                    {
                        name = "Meifan";
                    }
                    newstr = chartalk1 + name + "|" + speech + endCurlyBraces;
                }
                outfile.WriteLine(newstr);
            }

            if (!isTranscriptOnly)
            {
                outfile.WriteLine(tabber2);
                if (character != null)
                {
                    outfile.WriteLine(category + bondStories + endSquareBraces);
                    outfile.WriteLine(category + character + " " + bondStories + endSquareBraces);
                }
                else if (mode == "m")
                {
                    outfile.WriteLine(category + mainStories + endSquareBraces);
                }
                else if (mode == "e")
                {
                    outfile.WriteLine(category + eventStories + endSquareBraces);
                    for (int i=0; i < schools.Length; i++)
                    {
                        outfile.WriteLine(category + schools[i] + " " + stories + endSquareBraces);
                    }
                }
                outfile.WriteLine(category + transcripts + endSquareBraces);
            }

            System.Diagnostics.Process.Start(@"C:\Windows\system32\notepad.exe", "transcript.txt");
        }
    }
}
