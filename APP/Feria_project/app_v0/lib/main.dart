import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'camera.dart';

Future<void> main() async {
  // Ensure that plugin services are initialized so that `availableCameras()`
  // can be called before `runApp()`
  WidgetsFlutterBinding.ensureInitialized();

  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  // Get a specific camera from the list of available cameras.
  final firstCamera = cameras.first;

  runApp(
    MaterialApp(
      home: GetProduct(firstCamera),
    ),
  );
}

//void main() => runApp(MaterialApp(
//      home: GetProduct(),
//    ));

//creando un widget
class GetProduct extends StatelessWidget {
  final firstCamera;

  GetProduct(this.firstCamera);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      //estructura basica scaffold
      appBar: AppBar(
        title: Text("Identificar producto [NN]"),
        centerTitle: true,
        backgroundColor: Colors.blue[600],
        elevation: 0,
      ), //esto es un widget
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          FlatButton(
            color: Colors.blue[300],
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) =>
                        TakePictureScreen(camera: firstCamera)),
              );
            },
            child: Text(
              'Productos en general',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                letterSpacing: 2.0,
              ),
            ),
          ),
          FlatButton(
            color: Colors.blue[300],
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) =>
                        TakePictureScreen(camera: firstCamera)),
              );
            },
            child: Text(
              'Vestuario',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                letterSpacing: 2.0,
              ),
            ),
          ),
        ],
      ),
      backgroundColor: Colors.blue[400],
    );
  }
}

class ImageNetworkGeneral extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

class ImageNetworkClothes extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
