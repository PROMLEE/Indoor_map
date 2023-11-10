import 'dart:async';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';
import 'package:geolocator/geolocator.dart';

class NaverMapApp extends StatelessWidget {
  const NaverMapApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Completer<NaverMapController> mpaControllerCompleter = Completer();
<<<<<<< Updated upstream
=======
    final marker = NMarker(
        id: 'currentPosition',
        position: NLatLng(position.latitude, position.longitude));
    final onMarkerInfoWindow =
        NInfoWindow.onMarker(id: marker.info.id, text: "건물정보API필요할듯");
>>>>>>> Stashed changes
    //NCircleOverlay(id: "currentPosition", center: NLatLng(position.latitude,position.longitude));
    return MaterialApp(
      home: Scaffold(
        body: Column(
          children: <Widget>[
            Row(
              children: [
                Container(
                  margin: const EdgeInsets.all(30),
                  child: const Text("실내\n길 찾기.",
                      style: TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: Color.fromARGB(255, 49, 49, 49),
                      )),
                ),
              ],
            ),
            Expanded(
              child: NaverMap(
<<<<<<< Updated upstream
                options: const NaverMapViewOptions(
                  // initialCameraPosition: NCameraPosition(
                  //   target: NLatLng(marker.position.latitude,marker.position.longitude),
                  //   zoom: 15,
                  //   bearing: 0,
                  //   tilt: 0,
                  // ),
=======
                options: NaverMapViewOptions(
                  initialCameraPosition: NCameraPosition(
                    target: NLatLng(
                        marker.position.latitude, marker.position.longitude),
                    zoom: 15,
                    bearing: 0,
                    tilt: 0,
                  ),
>>>>>>> Stashed changes
                  rotationGesturesEnable: false,
                  indoorEnable: true,
                  locationButtonEnable: false,
                  consumeSymbolTapEvents: false,
                ),
                onMapReady: (controller) async {
                  mpaControllerCompleter.complete(controller);
<<<<<<< Updated upstream
                  log("네이버맵 준비완료!", name : "onMapReady");
=======
                  log("네이버맵 준비완료!", name: "onMapReady");
                  controller.addOverlay(marker);
                  marker.openInfoWindow(onMarkerInfoWindow);
>>>>>>> Stashed changes
                },
              ),
            ),
            //여기에 위젯 추가
          ],
        ),
      ),
    );
  }
}
