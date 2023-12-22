import 'dart:async';
import 'dart:developer';
import 'package:navermaptest01/map_render.dart';
import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import "package:permission_handler/permission_handler.dart";

class NaverMapApp extends StatefulWidget {
  const NaverMapApp({Key? key}) : super(key: key);

  @override
  State<NaverMapApp> createState() => _NaverMapAppState();
}

class _NaverMapAppState extends State<NaverMapApp> {
//서버에서 가져오는 시간이 있으니까 async랑 await을 써줘야함
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

//DB에서 가져온 데이터를 보여줄때는 FutureBuilder나 StreamBuilder를 사용해야함
//StreamBuilder는 데이터가 지속적으로 변해야할때 사용
//FutureBuilder는 한번만 가져오면 될때 사용
//그러면 우리는 좌표만 딱 해서 하면되니까 FutureBuilder사용
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
                  child: const Text(
                    "실내\n길 찾기.\n건물을 선택하세요.",
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 49, 49, 49),
                    ),
                  ),
                ),
              ],
            ),
            Expanded(
              child: FutureBuilder(
                future: getBuildingsData(),
                builder: (BuildContext context, AsyncSnapshot snapshot) {
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
                                    var data = result.data(); // 여기서 데이터를 미리 추출
                                    log("$data");
                                    // result.data()를 통해 데이터에 접근 가능
                                    if (data != null) {
                                      // 데이터가 null이 아닌 경우에만 Navigator.push 호출
                                      if (!mounted) return;

                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) => ThirdScreen(
                                            data: data,
                                            documentId: documentId,
                                          ), // 데이터를 ThirdScreen으로 전달
                                        ),
                                      );
                                    }
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
            //여기에 위젯 추가
          ],
        ),
      ),
    );
  }
}
