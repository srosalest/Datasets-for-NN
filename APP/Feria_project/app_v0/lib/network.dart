import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:async';
import 'dart:convert';

final url = "http://164.90.149.7:5000/";

Future<Prediction> requestPrediction(String imagePath) async {
  List<int> imageBytes = File(imagePath).readAsBytesSync();
  final http.Response response = await http.post(
    url,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'image': base64Encode(imageBytes),
    }),
  );
  if (response.statusCode == 200) {
    return Prediction.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to get prediction.');
  }
}

class Prediction {
  String waste;
  String trashnet;
  String brand;
  String clothes;

  Prediction({this.waste, this.trashnet, this.brand, this.clothes});

  factory Prediction.fromJson(Map<String, dynamic> json) => Prediction(
      waste: json["waste"],
      trashnet: json["trashnet"],
      brand: json["brand"],
      clothes: json["clothes"]);

  Map<String, dynamic> toJson() => {
        "waste": waste,
        "trashnet": trashnet,
        "brand": brand,
        "clothes": clothes
      };
}

class DisplayPictureScreen extends StatelessWidget {
  final Future<Prediction> prediction;
  //final String imagePath; this.imagePath

  const DisplayPictureScreen({Key key, this.prediction}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Realizando consulta')),
      body: Center(
        child: FutureBuilder<Prediction>(
          future: prediction,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              //Text(snapshot.data.waste)
              return Column(
                children: <Widget>[
                  Text(snapshot.data.waste),
                  Text(snapshot.data.trashnet),
                  Text(snapshot.data.brand),
                  Text(snapshot.data.clothes),
                ],
              );
            } else if (snapshot.hasError) {
              return Text("${snapshot.error}");
            }
            return CircularProgressIndicator();
          },
        ),
      ),
    );
  }
}

//request es img base64
//reply 'waste': 'organic',
//  'trashnet' : 'empty',
//     'brand' : 'empty',
//   'clothes' : 'empty'

//todo: cambiar los nombres e implementar la diferenciacion entre la ropa y el general
