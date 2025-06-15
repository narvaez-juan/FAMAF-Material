package parser;

import feed.Article;
import feed.Feed;
import java.io.StringReader;
import java.util.Date;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

public class RssParser extends GeneralParser{
    String siteName;

    //Constructor de la clase
    public RssParser(String source, String siteName)
    {
        this.source = source;
        this.siteName = siteName;
    }

    //Método get de la clase
    public String getSource()
    {
        return source;
    }

    @Override
    public Feed parse() throws Exception
    {
        Feed feed = new Feed(this.siteName);

        //parseo del contenido xml
        Document xmlDoc = loadXMLFromString(source);

        //lista de item's
        NodeList articlesList = xmlDoc.getElementsByTagName("item");

        for (int temp = 0, list_len = articlesList.getLength(); temp < list_len; temp++) {
            
            Node nNode = articlesList.item(temp);
            
            //extrae los atributos que nos interesa de cada item
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {     
                Element eElement = (Element) nNode;
                String title = eElement.getElementsByTagName("title").item(0).getTextContent();
                String text = eElement.getElementsByTagName("description").item(0).getTextContent();
                Date publicationDate = new Date(eElement.getElementsByTagName("pubDate").item(0).getTextContent());
                String link = eElement.getElementsByTagName("link").item(0).getTextContent();
                
                //agrega un artículo al feed
                feed.addArticle(new Article(title, text, publicationDate, link));
             }
        }
        return feed;
    }

    private static Document loadXMLFromString(String xml) throws Exception
    {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        //parseo de String a xml
        InputSource inputSource = new InputSource(new StringReader(xml));
        //parseo de xml a Document
        return builder.parse(inputSource);
    }
}