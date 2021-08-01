using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace t2f
{
    class Program
    {
        #region Constants
        // init constants
        static string chartalk1 = "{{CharTalk|";
        static string endCurlyBraces = "}}";
        static string new_part = "|-|\n";
        static string title1 = "Chapter ";
        static string title1e = "Part ";
        static string title1final = "Final Part";
        static string title2 = "=\n<span style=\"font-weight: bold; font-size: 20px;\" >";
        static string titleEnd = "</span>";
        static string subtitle1 = "<br><span style=\"font-weight: bold; font-size: 16px;\" >";
        static string divider = "<hr>";
        static string quoteHead = "{{Quote|";
        static string category = "[[Category:";
        static string endSquareBraces = "]]";
        static string tabber1 = "<tabber>";
        static string tabber2 = "</tabber>";
        static string bondStories = "Bond Stories";
        static string mainStories = "Main Stories";
        static string eventStories = "Event Stories";
        static string stories = "Stories";
        static string transcripts = "Transcripts";
        static string arcana = "''(Part 1 and Part 2 of [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Third Part: Arcana Arcadia|Arcana Arcadia]] Stage Girl bond stories are viewable in the Gallery under [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Intermission|Arcana Arcadia - Intermission]].)''";

        #endregion

        #region Private Properties
        private static readonly HttpClient client = new HttpClient();
        #endregion

        #region API Methods
        private static async Task<dynamic> GetJson(string url)
        {
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
            client.DefaultRequestHeaders.Add("User-Agent", ".NET Foundation Repository Reporter");

            var stringTask = client.GetStringAsync(url);
            var json = await stringTask;
            return JObject.Parse(json);
        }


        private static async Task<dynamic> GetStory(string code)
        {
            var json = await GetJson("https://karth.top/api/adventure/ww/" + code + ".json");
            return json;
        }

        private static async Task<dynamic> GetCharaNames()
        {
            var json = await GetJson("https://karth.top/api/adventure_chara_name.json");
            return json;
        }

        private static async Task<dynamic> GetDress(string code)
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

        private static async Task<bool> ProcessScript(string code)
        {
            var story = await GetStory(code);
            var charaNames = await GetCharaNames();
            string outputLine = "";
            using var outfile = System.IO.File.AppendText("transcript.txt");
            foreach (var item in story.script)
            {
                outputLine = "";
                JToken line = item.Value;
                if (line.HasValues)
                {
                    string type = (string)line["type"];
                    JToken args = line["args"];
                    if (args.Type == JTokenType.Array) 
                        continue;
                    JToken characterId = args["characterId"];
                    if (type == "message")
                    {
                        string nameId = (string)args["nameId"];
                        if ((string)nameId != "0")
                        {
                            string name = (string)charaNames[Convert.ToString(nameId)]["en"];
                            string speech = (string)args["body"]["en"];
                            int b = name.IndexOf('(');
                            if (b != -1)
                            {
                                speech = "'''(" + name[(b + 1)..] + "'''<br>" + speech;
                                name = name[..(b - 1)];
                            }
                            if (name.Contains("Mei Fan")) 
                                name.Replace("Mei Fan", "Meifan");
                            outputLine = chartalk1 + name + "|" + speech + endCurlyBraces;
                        }
                        else if (characterId.Type == JTokenType.Integer)
                        {
                            if ((int)characterId == 0)
                            {
                                outputLine = chartalk1 + "|" + (string)args["body"]["en"] + endCurlyBraces;
                            }
                            else
                            {
                                string name = GetNameFromCharacterId((int)characterId, charaNames, story.setting);
                                outputLine = chartalk1 + name + "|" + (string)args["body"]["en"] + endCurlyBraces;
                            }
                        }
                        else if (characterId.Type == JTokenType.Array)
                        {
                            string name = "";
                            foreach (var chara in characterId)
                            {
                                string charaName = GetNameFromCharacterId((int)chara, charaNames, story.setting);
                                name += charaName + " & ";

                            }
                            outputLine = chartalk1 + name[..^3] + "|" + (string)args["body"]["en"] + endCurlyBraces;
                        }
                    } 
                    else if (type == "showTitle")
                    {
                        var tempTitle = subtitle1;
                        if (item.Name == "3") 
                            tempTitle = title2;
                        outputLine = tempTitle + (string)args["body"]["en"] + titleEnd;
                        
                    }
                    else if (type == "fadeOut")
                    {
                        outputLine = divider;
                    }
                    if (outputLine != "")
                        outfile.WriteLine(outputLine);
                }
            }
            return true;
        }

        private static string GetNameFromCharacterId(int characterId, dynamic charaNames, JObject setting)
        {
            string dressCode = (string)setting["character"][characterId-1];
            string name = (string)charaNames[dressCode[..3]]["en"];
            if (name.Contains("Mei Fan"))
                name.Replace("Mei Fan", "Meifan");
            return name;
        }

        #endregion
        static async Task Main(string[] args)
        {
            string code = args[0];

            System.IO.File.Create("transcript.txt").Close();
            
            bool noMeta = false;
            if (args[^1] == "--nometa")
            {
                noMeta = true;
            }

            if (code[0] == '1')
            {
                // Main Story: name of story and number of chapters to process should be provided after argument "-m"
                int numChapters = 0;
                string storyTitle = "";
                for (var i=0; i < args.Length; i++)
                {
                    if (args[i] == "-m")
                    {
                        storyTitle = args[i + 1];
                        numChapters = Int32.Parse(args[i + 2]);
                    }
                }
                if (!noMeta)
                {
                    string header = "";
                    header += "==Transcript==\n" + tabber1;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText("transcript.txt"))
                        outfile.WriteLine(header);
                }

                int newCode = Int32.Parse(code);
                for (var i=0; i < numChapters; i++)
                {
                    string num = (newCode % 100).ToString();
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText("transcript.txt"))
                    {
                        outfile.WriteLine(new_part + title1e + num + title2 + storyTitle + titleEnd);
                        outfile.WriteLine(subtitle1[4..] + title1e + num + titleEnd);
                    }
                        
                    await ProcessScript(newCode.ToString());
                    newCode++;
                }
                if (!noMeta)
                {
                    string footer = "";
                    footer += tabber2 + "\n" + category + mainStories + endSquareBraces;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText("transcript.txt"))
                        outfile.WriteLine(footer);
                }
            }
            else if (code[1] == '5')
            {
                // Event Story: 6 chapters
            }
            else if (code[1] == '3')
            {
                // Bond Story: 301,302 are Chapter 1,2 ; 311,312 are Bond Level 15 Talk, Bond Level 30 Talk
            }
            else
            {
                Console.WriteLine("Code is incorrect (not beginning with 1, 3, or 5)");
                Environment.Exit(1);
            }
            //var story = await GetStory(code);
            //var charaNames = await GetCharaNames();
            
            //await ProcessScript(story, charaNames);
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
                        newstr = new_part + title1final + title2 + line[3..] + titleEnd;
                    }
                    else if (int.TryParse(num.ToString(), out _))
                    {
                        newstr = new_part + title1 + num + title2 + line[3..] + titleEnd;
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
                        newstr = subtitle1[4..] + line[2..] + titleEnd;
                    }
                    else if (line[1] == '.')
                    {
                        newstr = "<hr>";
                    }
                    else
                    {
                        newstr = subtitle1 + line[1..] + titleEnd;
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
