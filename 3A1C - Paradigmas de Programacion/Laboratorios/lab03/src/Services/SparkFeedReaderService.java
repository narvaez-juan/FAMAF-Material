package Services;

import feed.Article;
import feed.Feed;
import httpRequest.HttpRequester;
import interfaces.IFeedReaderService;
import namedEntity.NamedEntity;
import namedEntity.heuristic.Heuristic;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import parser.SubscriptionParser;
import subscription.SingleSubscription;
import subscription.Subscription;

import java.util.*;

public class SparkFeedReaderService implements IFeedReaderService {
    private HttpRequester requester;
    private SubscriptionParser subscriptionParser;
    private SparkSession spark;
    private JavaSparkContext jsc;

    public SparkFeedReaderService(
            HttpRequester requester,
            SubscriptionParser subscriptionParser) {
        this.requester = requester;
        this.subscriptionParser = subscriptionParser;
        
        // Configurar Spark
        this.spark = SparkSession
                .builder()
                .appName("FeedReader")
                .master("spark://fran-MAX-G0101:7077") // Cambiar a local[*] para pruebas locales
                .getOrCreate();
        this.jsc = new JavaSparkContext(spark.sparkContext());
    }

    @Override
    public void printFeedResults() {
        try {
            Subscription subscriptionData = this.subscriptionParser.parse();
            List<SingleSubscription> subscriptions = subscriptionData.getSubscriptionsList();

            // Convertir suscripciones a pares (subscription, paramIndex)
            List<Map.Entry<SingleSubscription, Integer>> tasks = new ArrayList<>();
            for (SingleSubscription subscription : subscriptions) {
                for (int i = 0; i < subscription.getUrlParamsSize(); i++) {
                    tasks.add(new AbstractMap.SimpleEntry<>(subscription, i));
                }
            }

            // Creación del RDD

            HttpRequester requesterCopy = this.requester;

            JavaRDD<Feed> feedsRDD = jsc.parallelize(tasks)
                .map(entry -> IFeedReaderService.getParsedFeed(
                        entry.getKey(),
                        entry.getValue(),
                        requesterCopy));

            // Imprimir resultados
            feedsRDD.collect().forEach(Feed::prettyPrint);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        } finally {
            if (spark != null) {
                spark.close();
            }
        }
    }

    @Override
    public void printFeedEntitiesByHeuristic(Heuristic heuristic) {
        try {
            Subscription subscriptionData = this.subscriptionParser.parse();
            List<SingleSubscription> subscriptions = subscriptionData.getSubscriptionsList();

            // Paralelizar la descarga y parseo de feeds
            List<Map.Entry<SingleSubscription, Integer>> tasks = new ArrayList<>();
            for (SingleSubscription subscription : subscriptions) {
                for (int i = 0; i < subscription.getUrlParamsSize(); i++) {
                    tasks.add(new AbstractMap.SimpleEntry<>(subscription, i));
                }
            }

            // Creación del RDD

            HttpRequester requesterCopy = this.requester;

            JavaRDD<Article> articlesRDD = jsc.parallelize(tasks)
                .flatMap(entry -> {
                    try {
                        Feed feed = IFeedReaderService.getParsedFeed(
                                entry.getKey(),
                                entry.getValue(),
                                requesterCopy);
                        return feed.getArticleList().iterator(); // lo vuelve iterable
                    } catch (Exception e) {
                        return Collections.emptyIterator();
                    }
                });

            // Procesar entidades nombradas en paralelo
            JavaRDD<NamedEntity> entitiesRDD = articlesRDD
                .mapPartitions(articles -> {
                    List<NamedEntity> entities = new ArrayList<>();
                    articles.forEachRemaining(article -> { //posibles null
                        article.computeNamedEntities(heuristic);
                        entities.addAll(article.getNamedEntitiesList());
                    });
                    return entities.iterator(); // igual que arriba
                });

            // Agrupar y contar entidades
            Map<String, Integer> entityCounts = entitiesRDD
                .mapToPair(entity -> new Tuple2<>(entity.getName(), entity.getFrequency())) //mapea a tupla
                .reduceByKey(Integer::sum) // reduceByKey suma las frecuencias de las entidades con el mismo nombre)
                .collectAsMap();

            // Imprimir resultados ordenados
            entityCounts.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue()));
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        } finally {
            if (spark != null) {
                spark.close();
            }
        }
    }
}
