using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Linq;

namespace t2f
{
    class Program
    {
        #region Constants
        // init constants
        static string chartalk1 = "{{CharTalk|";
        static string endCurlyBraces = "}}";
        static string newPart = "|-|\n";
        static string title1 = "Chapter ";
        static string title1e = "Part ";
        static string title1final = "Final Part";
        static string title2 = "<span style=\"font-weight: bold; font-size: 20px;\" >";
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

        static Dictionary<int, string> charaCodes = new Dictionary<int, string> {
            { 101, "Karen Aijo" },
            { 102, "Hikari Kagura" },
            { 103, "Mahiru Tsuyuzaki" },
            { 104, "Claudine Saijo" },
            { 105, "Maya Tendo" },
            { 106, "Junna Hoshimi" },
            { 107, "Nana Daiba" },
            { 108, "Futaba Isurugi" },
            { 109, "Kaoruko Hanayagi" },
            { 201, "Tamao Tomoe" },
            { 202, "Ichie Otonashi" },
            { 203, "Fumi Yumeoji" },
            { 204, "Rui Akikaze" },
            { 205, "Yuyuko Tanaka" },
            { 301, "Aruru Otsuki" },
            { 302, "Misora Kano" },
            { 303, "Lalafin Nonomiya" },
            { 304, "Tsukasa Ebisu" },
            { 305, "Shizuha Kocho" },
            { 401, "Akira Yukishiro" },
            { 402, "Michiru Otori" },
            { 403, "Liu Mei Fan" },
            { 404, "Shiori Yumeoji" },
            { 405, "Yachiyo Tsuruhime" },
            { 501, "Koharu Yanagi" },
            { 502, "Suzu Minase" },
            { 503, "Hisame Honami" },
            { 802, "Elle Nishino" },
            { 803, "Andrew" }
        };

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

        private static async Task<bool> ProcessScript(string code, string filename)
        {
            var story = await GetStory(code);
            var charaNames = await GetCharaNames();
            string outputLine = "";
            using var outfile = System.IO.File.AppendText(filename);
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
                            // single speaker
                            string name = (string)charaNames[Convert.ToString(nameId)]["en"];
                            string speech = (string)args["body"]["en"];
                            int b = name.IndexOf('(');
                            if (b != -1)
                            {
                                speech = "'''(" + name[(b + 1)..] + "'''<br>" + speech;
                                name = name[..(b - 1)];
                            }
                            if (name.Contains("Mei Fan")) 
                                name = name.Replace("Mei Fan", "Meifan");
                            outputLine = chartalk1 + name + "|" + speech + endCurlyBraces;
                        }
                        else if (characterId.Type == JTokenType.Integer)
                        {
                            if ((int)characterId == 0)
                            {
                                // sound effect
                                outputLine = chartalk1 + "|" + (string)args["body"]["en"] + endCurlyBraces;
                            }
                            else
                            {
                                // single speaker identifiable from live2d
                                string name = GetNameFromCharacterId((int)characterId, charaNames, story.setting);
                                outputLine = chartalk1 + name + "|" + (string)args["body"]["en"] + endCurlyBraces;
                            }
                        }
                        else if (characterId.Type == JTokenType.Array)
                        {
                            // multiple speakers identifiable from live2ds
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
                name = name.Replace("Mei Fan", "Meifan");
            return name;
        }

        #endregion
        static async Task Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("t2f.exe -dresscode [-a] [-o filename]\nt2f.exe eventstorycode -e 12345 [-o filename] \nt2f.exe mainstorycode -m storyTitle numChapters [-o filename] [--nometa]");
                Environment.Exit(0);
            }
            string code = args[0];

            string filename = "transcript.txt";

            for (var i = 0; i < args.Length; i++)
            {
                if (args[i] == "-o")
                    filename = args[i + 1];
            }

            System.IO.File.Create(filename).Close();
            
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
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(header);
                }

                long newCode = (long)Convert.ToDouble(code);
                for (var i=0; i < numChapters; i++)
                {
                    string num = (newCode % 100).ToString();
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                    {
                        outfile.WriteLine(newPart + title1e + num + "=" + title2 + storyTitle + titleEnd);
                        outfile.WriteLine(subtitle1[4..] + title1e + num + titleEnd);
                    }
                        
                    await ProcessScript(newCode.ToString(), filename);
                    newCode++;
                }
                if (!noMeta)
                {
                    string footer = "";
                    footer += tabber2 + "\n" + category + mainStories + endSquareBraces;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(footer);
                }
            }
            else if (code[0] == '5')
            {
                // Event Story: 6 chapters, schools involved provided as arg after -e ie. 13 = seisho frontier
                if (!noMeta)
                {
                    string header = "";
                    header += tabber1;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(header);
                }
                long newCode = (long)Convert.ToDouble(code);
                for (var i = 0; i < 6; i++)
                {
                    string num = (newCode % 100).ToString();
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                    {
                        if (i == 5)
                        {
                            outfile.WriteLine(newPart + title1final + "=");
                        }
                        else
                        {
                            outfile.WriteLine(newPart + title1e + num + "=");
                        }
                    }
                    await ProcessScript(newCode.ToString(), filename);
                    newCode++;
                }
                if (!noMeta)
                {
                    string schools = "";
                    for (var i = 0; i < args.Length; i++)
                    {
                        if (args[i] == "-e")
                        {
                            schools = args[i + 1];
                        }
                    }
                    string footer = "";
                    footer += tabber2 + "\n" + category + eventStories + endSquareBraces;
                    if (schools.Contains("1"))
                        footer += "\n" + category + "Seisho Music Academy " + stories + endSquareBraces;
                    if (schools.Contains("2"))
                        footer += "\n" + category + "Rinmeikan Girls School " + stories + endSquareBraces;
                    if (schools.Contains("3"))
                        footer += "\n" + category + "Frontier School of Arts " + stories + endSquareBraces;
                    if (schools.Contains("4"))
                        footer += "\n" + category + "Siegfeld Institute of Music " + stories + endSquareBraces;
                    if (schools.Contains("5"))
                        footer += "\n" + category + "Seiran General Art Institute " + stories + endSquareBraces;
                    footer += "\n" + category + transcripts + endSquareBraces;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(footer);
                }
            }
            else if (code[0] == '-')
            {
                // Bond Story: 30[code]1,30[code]2 are Chapter 1,2 ; 31[code]1,31[code]2 are Bond Level 15 Talk, Bond Level 30 Talk
                code = code[1..];
                if (!noMeta)
                {
                    JObject dress = await GetDress(code);
                    string header = "";
                    string profile = (string)dress["basicInfo"]["profile"]["en"];
                    header += quoteHead + profile + endCurlyBraces;
                    if (args.Contains("-a"))
                        header += "\n" + arcana;
                    header += "\n" + tabber1;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(header);
                }
                for (var i = 1; i < 5; i++)
                {
                    string newCode = "";
                    if (i < 3)
                    {
                        if (args.Contains("-a"))
                            title1 = "Part ";
                        using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                            outfile.WriteLine(newPart + title1 + i + "=");
                        newCode = "30" + code + i;
                    }
                    else if (i == 3)
                    {
                        using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                            outfile.WriteLine(newPart + "Bond Level 15 Talk=");
                        newCode = "31" + code + 1;
                    }
                    else if (i == 4)
                    {
                        using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                            outfile.WriteLine(newPart + "Bond Level 30 Talk=");
                        newCode = "31" + code + 2;
                    }

                    await ProcessScript(newCode.ToString(), filename);
                }
                if (!noMeta)
                {
                    string footer = "";
                    footer += tabber2 + "\n" + category + bondStories + endSquareBraces;
                    footer += "\n" + category + charaCodes[Int32.Parse(code[..3])] + " " + bondStories + endSquareBraces;
                    footer += "\n" + category + transcripts + endSquareBraces;
                    using (System.IO.StreamWriter outfile = System.IO.File.AppendText(filename))
                        outfile.WriteLine(footer);
                }
            }
            else
            {
                Console.WriteLine("Code is incorrect (not beginning with -, 3, or 5)");
                Environment.Exit(1);
            }

            System.Diagnostics.Process.Start(@"C:\Program Files (x86)\Notepad++\notepad++.exe", filename);
        }
    }
}
