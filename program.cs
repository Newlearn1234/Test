// using System;
// partial class Program
// {
//     static void Main()
//     {
//         Console.WriteLine("Hello, World!");
//     }
// }

using System;
using System.Xml;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, World!"); // Add this line to print "Hello, World!"

        // Specify the path to your XML file
        string xmlFilePath = "extra.xml"; // Replace with your XML file's path

        try
        {
            // Load the XML document
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load(xmlFilePath);

            // Access XML elements and attributes
            XmlNodeList nodes = xmlDoc.SelectNodes("/root/element");

            foreach (XmlNode node in nodes)
            {
                string value = node.InnerText;
                Console.WriteLine(value);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: " + ex.Message);
        }
    }
}

