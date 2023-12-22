// ignore_for_file: must_be_immutable

import 'dart:async';
import 'dart:developer';
import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:navermaptest01/owner.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import "package:permission_handler/permission_handler.dart";

class OwnerChoiceBuilding extends StatefulWidget {
  const OwnerChoiceBuilding({Key? key}) : super(key: key);

  @override
  State<OwnerChoiceBuilding> createState() => _OwnerChoiceBuildingState();
}

class _OwnerChoiceBuildingState extends State<OwnerChoiceBuilding> {
  Future<List<DocumentSnapshot>> getBuildingsData() async {
    final firestore = FirebaseFirestore.instance;
    QuerySnapshot querySnapshot = await firestore.collection('buildings').get();
    return querySnapshot.docs;
  }

  NMarker createMarker(DocumentSnapshot buildingData) {
    var data = buildingData.data() as Map<String, dynamic>;
    var lat = data['Latitude'] as double;
    var lon = data['Longitude'] as double;
    var buildingName = data['BuildingName'];
    var marker = NMarker(
      id: buildingName,
      position: NLatLng(lat, lon),
    );
    return marker;
  }

  void permission() async {
    var status = await Permission.locationWhenInUse.status;
    if (!status.isGranted) {
      await [Permission.locationWhenInUse].request(); // [] 권한배열에 권한을 작성
    }
  }

  bool isSwitched = false;

  @override
  Widget build(BuildContext context) {
    permission();
    return MaterialApp(
      home: Scaffold(
        body: Column(
          children: <Widget>[
            Row(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 10, top: 15),
                  child: const Text("건물을\n선택하세요.",
                      style: TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: Color.fromARGB(255, 49, 49, 49),
                      )),
                ),
              ],
            ),
            Expanded(
              child: FutureBuilder(
                future: getBuildingsData(),
                builder: (BuildContext context1, AsyncSnapshot snapshot) {
                  //가져온 데이터는 snapshot에 저장되어있음
                  //snapshot은 object타입이라 바로 접근 불가
                  //따라서 Map으로 변환
                  log("홀리뱅$snapshot");
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  } else if (snapshot.hasError) {
                    return const Center(
                        child: Text('Error: 데이터를 가져오는 데 실패했습니다.'));
                  } else {
                    // 데이터를 사용하여 NaverMap 위젯을 구성합니다.
                    return snapshot.hasData
                        ? //데이터 가져오는데 시간이 걸리니까 빌드속도보다 느리면 null이라서 hasData키워드 사용
                        NaverMap(
                            options: const NaverMapViewOptions(
                              rotationGesturesEnable: false,
                              indoorEnable: true,
                              locationButtonEnable: true,
                              consumeSymbolTapEvents: false,
                            ),
                            onMapTapped: (NPoint point, NLatLng latLng) async {
                              log("${latLng.latitude}");
                              log("${latLng.longitude}");
                              // final marker =
                              //     NMarker(id: "test", position: latLng);
                              // final onMarkerInfoWindow = NInfoWindow.onMarker(
                              //     id: marker.info.id,
                              //     text: "해당 건물이 맞으시면\n 마커를 눌러주세요!");
                              // _controller.addOverlay(marker);
                              // marker.openInfoWindow(onMarkerInfoWindow);
                              // marker.setOnTapListener(
                              // (marker) {
                              // log("${marker.position}");
                              showDialog(
                                context: context,
                                builder: (BuildContext context) {
                                  String buildingName = "";
                                  String floorNumber = "";
                                  String basementNumber = "";
                                  // NLatLng markerPosition = marker.position;
                                  NLatLng markerPosition = latLng;
                                  return StatefulBuilder(
                                    builder: (BuildContext context,
                                        StateSetter setState) {
                                      return AlertDialog(
                                        title: const Text(
                                          "건물 정보 입력",
                                          style: TextStyle(
                                            fontSize: 30,
                                            fontWeight: FontWeight.bold,
                                            color:
                                                Color.fromARGB(255, 49, 49, 49),
                                          ),
                                        ),
                                        content: SingleChildScrollView(
                                          child: Column(
                                            mainAxisAlignment:
                                                MainAxisAlignment.start,
                                            children: [
                                              Row(
                                                crossAxisAlignment:
                                                    CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                      "위도 : ${latLng.latitude}"),
                                                ],
                                              ),
                                              Row(
                                                crossAxisAlignment:
                                                    CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                      "경도 : ${latLng.longitude}"),
                                                ],
                                              ),
                                              Row(
                                                mainAxisAlignment:
                                                    MainAxisAlignment.start,
                                                children: [
                                                  const Text("건물에 지하가 있나요?"),
                                                  Switch(
                                                    value: isSwitched,
                                                    onChanged: (value) {
                                                      setState(() {
                                                        isSwitched = value;
                                                      });
                                                    },
                                                    activeColor: Colors.green,
                                                  )
                                                ],
                                              ),
                                              TextField(
                                                onChanged: (value) {
                                                  buildingName = value;
                                                },
                                                decoration:
                                                    const InputDecoration(
                                                        labelText:
                                                            "건물명을 입력하세요"),
                                                keyboardType:
                                                    TextInputType.name,
                                              ),
                                              TextField(
                                                onChanged: (value) {
                                                  floorNumber = value;
                                                },
                                                decoration:
                                                    const InputDecoration(
                                                        labelText: "층수를 입력하세요"),
                                                keyboardType:
                                                    TextInputType.number,
                                              ),
                                              isSwitched
                                                  ? TextField(
                                                      onChanged: (value) {
                                                        basementNumber = value;
                                                      },
                                                      decoration:
                                                          const InputDecoration(
                                                              labelText:
                                                                  "지하 층수를 입력하세요"),
                                                      keyboardType:
                                                          TextInputType.number,
                                                    )
                                                  : Container(),
                                              const SizedBox(
                                                height: 30,
                                              ),
                                              OutlinedButton(
                                                onPressed: () {
                                                  //입력을 안했을때 처리
                                                  if (isSwitched == false) {
                                                    if (floorNumber == "" &&
                                                        buildingName == "") {
                                                      Fluttertoast.showToast(
                                                        msg: "층수와 건물명을 입력해주세요.",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (floorNumber ==
                                                        "") {
                                                      Fluttertoast.showToast(
                                                        msg: "층수를 입력해주세요.",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (buildingName ==
                                                        "") {
                                                      Fluttertoast.showToast(
                                                        msg: "건물명을 입력해주세요.",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else {
                                                      Navigator.of(context)
                                                          .push(
                                                        MaterialPageRoute(
                                                          builder: (BuildContext
                                                                  context) =>
                                                              Owner(
                                                            buildingName:
                                                                buildingName,
                                                            floorNumber:
                                                                int.parse(
                                                                    floorNumber),
                                                            nMarkerPosition:
                                                                markerPosition,
                                                          ),
                                                        ),
                                                      );
                                                    }
                                                  } else if (isSwitched) {
                                                    //true일때 따로 처리
                                                    if (floorNumber == "" &&
                                                        basementNumber == "" &&
                                                        buildingName == "") {
                                                      Fluttertoast.showToast(
                                                        msg:
                                                            "건물명, 층수, 지하층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (buildingName ==
                                                            "" &&
                                                        floorNumber == "" &&
                                                        basementNumber != "") {
                                                      Fluttertoast.showToast(
                                                        msg: "건물명, 층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (buildingName ==
                                                            "" &&
                                                        basementNumber == "" &&
                                                        floorNumber != "") {
                                                      Fluttertoast.showToast(
                                                        msg: "건물명, 지하층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (floorNumber ==
                                                            "" &&
                                                        basementNumber == "" &&
                                                        buildingName != "") {
                                                      Fluttertoast.showToast(
                                                        msg: "층수, 지하층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (buildingName ==
                                                        "") {
                                                      Fluttertoast.showToast(
                                                        msg: "건물명을 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (floorNumber ==
                                                        "") {
                                                      Fluttertoast.showToast(
                                                        msg: "층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else if (basementNumber ==
                                                        "") {
                                                      Fluttertoast.showToast(
                                                        msg: "지하 층수를 입력하세요",
                                                        toastLength:
                                                            Toast.LENGTH_SHORT,
                                                        gravity:
                                                            ToastGravity.BOTTOM,
                                                      );
                                                    } else {
                                                      Navigator.of(context)
                                                          .push(
                                                        MaterialPageRoute(
                                                          builder: (BuildContext
                                                                  context) =>
                                                              Owner(
                                                            buildingName:
                                                                buildingName,
                                                            floorNumber:
                                                                int.parse(
                                                                    floorNumber),
                                                            nMarkerPosition:
                                                                markerPosition,
                                                            basementNumber:
                                                                int.parse(
                                                                    basementNumber),
                                                          ),
                                                        ),
                                                      );
                                                    }
                                                  }
                                                },
                                                child: const Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Text(
                                                      "안내도 업로드\t",
                                                      style: TextStyle(
                                                        fontSize: 20,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                        color: Color.fromARGB(
                                                            255, 49, 49, 49),
                                                      ),
                                                    ),
                                                    Icon(
                                                        Icons
                                                            .upload_file_outlined,
                                                        color: Color.fromARGB(
                                                            255, 49, 49, 49),
                                                        size: 20)
                                                  ],
                                                ),
                                              )
                                            ],
                                          ),
                                        ),
                                      );
                                    },
                                  );
                                },
                              );
                              // },
                              // );
                            },
                            onMapReady: (controller) async {
                              final iconImage = await NOverlayImage.fromWidget(
                                  widget:
                                      const Icon(Icons.other_houses_outlined),
                                  size: const Size(48, 48),
                                  context: context);
                              for (var buildingData in snapshot.data) {
                                var marker = createMarker(buildingData);
                                marker.setIcon(iconImage); // 아이콘 이미지 설정
                                controller.addOverlay(marker); // 마커를 지도에 추가
                                // 마커 클릭 리스너 설정
                                marker.setOnTapListener(
                                  (NMarker marker) async {
                                    // 비동기 함수로 변경
                                    String documentId = buildingData["Latitude"]
                                            .toString()
                                            .substring(5, 9) +
                                        buildingData["Longitude"]
                                            .toString()
                                            .substring(5, 9);
                                    log(documentId);
                                    DocumentSnapshot result =
                                        await FirebaseFirestore.instance
                                            .collection('buildings')
                                            .doc(documentId)
                                            .get(); // await 키워드 사용
                                    var data = result.data() as Map<String,
                                        dynamic>; // 여기서 데이터를 미리 추출
                                    log("$data");
                                    // result.data()를 통해 데이터에 접근 가능
                                    // 데이터가 null이 아닌 경우에만 Navigator.push 호출
                                    if (!mounted) return;
                                    Navigator.of(context).push(
                                      MaterialPageRoute(
                                        builder: (BuildContext context) =>
                                            Owner(
                                          buildingName: data['BuildingName'],
                                          floorNumber: data['Floors'],
                                          nMarkerPosition: NLatLng(
                                            data["Latitude"],
                                            data["Longitude"],
                                          ),
                                          basementNumber: data['Basement'],
                                        ),
                                      ),
                                    );
                                    Navigator.pop(context1);
                                  },
                                );
                              }
                            },
                          )
                        : const Center(child: CircularProgressIndicator());
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
