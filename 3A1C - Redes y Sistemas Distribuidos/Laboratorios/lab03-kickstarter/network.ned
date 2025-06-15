// Sender App Layer
simple Generator
{
    parameters:
        volatile double generationInterval; // sec
        volatile int packetByteSize;
        @display("i=block/source");
    gates:
        output out;
}

simple Queue
{
    parameters:
        volatile int bufferSize;
        @display("i=block/queue;q=buffer");
    gates:
        input in;
        output out;
}

// Receiver App Layer
simple Sink
{
    parameters:
        @display("i=block/sink");
    gates:
        input in;
}

// Sender
module NodeTx
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
        output out;
    submodules:
        senderAppLayer: Generator {
            parameters:
                @display("p=75,50");
        }
        trSender: TransportSender {
            parameters:
                @display("p=75,190");
        }
    connections:
        in --> trSender.subnetwork$i; // Conexion que maneja los ACKs entrantes  // gen.out --> trSender.toApp;
        senderAppLayer.out --> trSender.appLayerIn; // Desde el generador de paquetes a la queue de capa de transporte
        trSender.subnetwork$o --> out; // Salida de la capa de transportes a paquetes  // trSender.toOut --> out;
}

// Receiver
module NodeRx
{
    parameters:
        @display("i=block/routing");
    gates:
        input in;
        output out;
    submodules:
        recAppLayer: Sink {
            parameters:
                @display("p=75,50");
        }
        trReceiver: TransportReceiver {
            parameters:
                @display("p=75,190");
        }
    connections:
        in --> trReceiver.subnetwork$i; // Conexion que maneja los paquetes de data entrantes del NodeTx  // in --> trReceiver.toOut;
        // Case study 1:
        trReceiver.appLayerOut --> { datarate = 0.5Mbps; } --> recAppLayer.in; // Desde la queue del receptor a la capa de aplicacion
        // Case study 2:
        // trReceiver.appLayerOut --> { datarate = 1Mbps; } --> recAppLayer.in; // Desde la queue del receptor a la capa de aplicacion
        trReceiver.subnetwork$o --> out; // Salida para mandar ACKs // trReceiver.toApp --> { datarate = 1Mbps; } --> sink.in;
}

// Nota del enunciado: Tener en cuenta que usando usando los operadores $i y $o se puede
// acceder a la entrada o salida independiente de una gate del tipo inout.

// TransportTx
simple TransportSender
{
    parameters:
        int bufferSize;
        int packetByteSize;
        double rtt @unit(s);
        double timeout @unit(s);
        @display("i=block/queue;q=buffer");
    gates:
        input appLayerIn; // toApp - input appLayer
        inout subnetwork; // toOut - input fromAppLayer
}

// TransportRx
simple TransportReceiver
{
    parameters:
        int bufferSize;
        int packetByteSize;
        @display("i=block/queue;q=buffer");
    gates:
        output appLayerOut;  // toApp
        inout subnetwork;  // toOut
}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,30");
        }
        dataQueue: Queue {
            @display("p=130,30");
        }
        ackQueue: Queue {
            @display("p=130,101");
        }
        nodeRx: NodeRx {
            @display("p=230,30");
        }
    connections:
        nodeTx.out --> { datarate = 1Mbps; delay = 100us; } --> dataQueue.in;
        // Case study 1:
        //dataQueue.out --> { datarate = 1Mbps; delay = 100us; } --> nodeRx.in;
        // Case study 2:
        dataQueue.out --> { datarate = 0.5Mbps; delay = 100us; } --> nodeRx.in;
        nodeRx.out --> { datarate = 1Mbps; delay = 100us; } --> ackQueue.in;
        ackQueue.out --> { datarate = 1Mbps; delay = 100us; } --> nodeTx.in;
}
