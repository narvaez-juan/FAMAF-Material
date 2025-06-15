package Services;

import feed.Article;
import feed.Feed;
import httpRequest.HttpRequester;
import interfaces.IFeedReaderService;
import namedEntity.NamedEntity;
import namedEntity.heuristic.Heuristic;
import parser.SubscriptionParser;
import subscription.SingleSubscription;
import subscription.Subscription;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.List;

public class FeedReaderService implements IFeedReaderService {
    private HttpRequester requester;
    private SubscriptionParser subscriptionParser;

    // Pseudo inyección de dependencias
    public FeedReaderService(
            HttpRequester requester,
            SubscriptionParser subscriptionParser) {
        this.requester = requester;
        this.subscriptionParser = subscriptionParser;
    }

    public void printFeedResults() {
        try {
            Subscription subscriptionData = this.subscriptionParser.parse();
            List<SingleSubscription> subscriptions = subscriptionData.getSubscriptionsList();

            for (SingleSubscription subscription : subscriptions) {
                for (int i = 0, params_size = subscription.getUrlParamsSize(); i < params_size; i++) {
                    Feed feed = IFeedReaderService.getParsedFeed(subscription, i, this.requester);
                    if (feed != null) {
                        feed.prettyPrint();
                    } else {
                        System.err.println("No se pudo parsear el feed para la suscripción: " + subscription.getUrl());
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.err.println("El archivo de suscripción no se encontró.");
        } catch (IOException e) {
            System.err.println("No se pudo leer todos los bytes del Path.");
        } catch (Exception e) {
            System.err.println("Error al parsear el feed: " + e.getMessage());
        }
    }

    public void printFeedEntitiesByHeuristic(Heuristic heuristic) {
        try {
            Subscription subscriptionData = this.subscriptionParser.parse();
            List<SingleSubscription> subscriptions = subscriptionData.getSubscriptionsList();

            for (SingleSubscription subscription : subscriptions) {
                for (int i = 0, params_size = subscription.getUrlParamsSize(); i < params_size; i++) {
                    Feed feed = IFeedReaderService.getParsedFeed(subscription, i, this.requester);
                    if (feed != null) {
                        for (Article article : feed.getArticleList()) {
                            article.computeNamedEntities(heuristic);
                            // Imprimir entidades
                            StringBuilder sb = new StringBuilder();
                            sb.append("Entidades encontradas:\n");
                            for (NamedEntity namedEntity : article.getNamedEntitiesList()) {
                                sb.append(namedEntity.toString()).append('\n');
                            }
                            System.out.print(sb.toString());
                        }
                    } else {
                        System.err.println("No se pudo parsear el feed para la suscripción: " + subscription.getUrl());
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.err.println("El archivo de suscripción no se encontró.");
        } catch (IOException e) {
            System.err.println("No se pudo leer todos los bytes del Path.");
        } catch (Exception e) {
            System.err.println("Error al parsear el feed: " + e.getMessage());
        }
    }
}
