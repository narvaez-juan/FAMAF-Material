import interfaces.IFeedReaderService;
import Services.SparkFeedReaderService;
import httpRequest.HttpRequester;
import namedEntity.heuristic.*;
import parser.SubscriptionParser;

import java.util.Scanner;

public class FeedReaderMain {

	private static void printHelp() {
		System.out.println("Please, call this program in correct way: FeedReader [-ne]");
	}

	private static Heuristic getHeuristic() {
		Scanner scanner = new Scanner(System.in);
		int opcion = -1;
		byte flag = -1;
		System.out.println("Ingresa la heuristica que quieres usar:");
		System.out.println("0: AllCapsHeuristic");
		System.out.println("1: QuickHeuristic");
		System.out.println("2: RandomHeuristic");
		while (flag < 0) {
			opcion = scanner.nextInt();
			if (opcion >= 0 && opcion <= 2) {
				flag = 1;
			} else {
				System.out.println("Esa opción no es válida. Intenta nuevamente.");
			}
		}

		Heuristic heuristic = null;
		switch (opcion) {
			case 0:
				System.out.println("Elegiste la heuristica AllCapsHeuristic");
				heuristic = new AllCapsHeuristic();
				break;
			case 1:
				System.out.println("Elegiste la heuristica QuickHeuristic");
				heuristic = new QuickHeuristic();
				break;
			case 2:
				System.out.println("Elegiste la heuristica RandomHeuristic");
				heuristic = new RandomHeuristic();
				break;
		}

		return heuristic;
	}

	public static void main(String[] args) {
		System.out.println("************* FeedReader version 2.0 *************");

		String subscriptionFilePath = "config/subscriptions.json";
		HttpRequester httpRequester = new HttpRequester();
		SubscriptionParser subscriptionParser = new SubscriptionParser(subscriptionFilePath);

		IFeedReaderService feedReaderService = new SparkFeedReaderService(httpRequester, subscriptionParser);

		// Si no se pasa ningún argumento
		if (args.length == 0) {
			// Ejecución
			feedReaderService.printFeedResults();
		}
		// Si se pasa un argumento (heuristica)
		else if (args.length == 1) {
			// Definir Heuristica a usar
			Heuristic heuristicToUse = getHeuristic();

			// Ejecución
			feedReaderService.printFeedEntitiesByHeuristic(heuristicToUse);
		} else {
			printHelp();
		}
	}
}
