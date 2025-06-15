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
    public Feed parse() throws Exception {
        if (source == null || source.trim().isEmpty()) {
            throw new IllegalArgumentException("Source cannot be null or empty");
        }

        Feed feed = new Feed(this.siteName);


        Document xmlDoc = null;
        try {
            xmlDoc = loadXMLFromString(source);
        } catch (Exception e) {
            System.out.println("Error parsing XML: " + e.getMessage());
            return feed; // Retorna feed vacío si hay error en el parseo
        }
        
        
        if (xmlDoc == null) {
            throw new Exception("Could not parse XML document");
        }

        NodeList articlesList = xmlDoc.getElementsByTagName("item");
        
        if (articlesList == null) {
            return feed; // Retorna feed vacío si no hay items
        }

        for (int temp = 0, list_len = articlesList.getLength(); temp < list_len; temp++) {
            Node nNode = articlesList.item(temp);
            
            if (nNode != null && nNode.getNodeType() == Node.ELEMENT_NODE) {     
                try {
                    Element eElement = (Element) nNode;
                    Node titleNode = eElement.getElementsByTagName("title").item(0);
                    Node textNode = eElement.getElementsByTagName("description").item(0);
                    Node dateNode = eElement.getElementsByTagName("pubDate").item(0);
                    Node linkNode = eElement.getElementsByTagName("link").item(0);
                    
                    // Verificar que todos los campos necesarios existan
                    if (titleNode == null || textNode == null || dateNode == null || linkNode == null) {
                        continue; // Salta este artículo si falta algún campo
                    }

                    String title = titleNode.getTextContent();
                    String text = textNode.getTextContent();
                    String dateStr = dateNode.getTextContent();
                    String link = linkNode.getTextContent();
                    
                    // Verificar que ningún contenido sea nulo
                    if (title == null || text == null || dateStr == null || link == null) {
                        continue;
                    }

                    Date publicationDate = new Date(dateStr);
                    feed.addArticle(new Article(title, text, publicationDate, link));
                } catch (Exception e) {
                    // Log error y continuar con el siguiente artículo
                    System.err.println("Error parsing article: " + e.getMessage());
                    continue;
                }
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