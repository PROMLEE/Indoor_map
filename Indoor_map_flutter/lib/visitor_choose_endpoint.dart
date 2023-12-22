import 'dart:convert';
import 'dart:developer';

import 'api_key.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dropdown_search/dropdown_search.dart';
import 'package:flutter/material.dart';
import 'package:navermaptest01/direction_guidance.dart';
import 'package:http/http.dart' as http;
import 'package:animated_custom_dropdown/custom_dropdown.dart';
import 'searchbox.dart';

void clearCache() {
  PaintingBinding.instance.imageCache.clear();
}

class VisitorChooseEndPoint extends StatefulWidget {
  final int selectedFloor;
  final int selectedLocation;
  final dynamic data;
  final String documentId;

  const VisitorChooseEndPoint({
    required this.selectedFloor,
    required this.selectedLocation,
    required this.data,
    required this.documentId,
    Key? key,
  }) : super(key: key);

  @override
  State<VisitorChooseEndPoint> createState() => _VisitorChooseEndPointState();
}

class _VisitorChooseEndPointState extends State<VisitorChooseEndPoint> {
  List<Store> _storeNames = []; // 매장명들을 저장할 List

  String imageUrl = '';

  int? _selectedFloorEndPoint;
  int? _selectedLocationEndPoint;
  int? _selectedTransportMethod;
  bool _showLocationDropdown = false;

  late String buildingName;

  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    //층, 출발지 선택을 할때마다 이미지를 가져오는 문제 찾음
    //문제라기보단 비효율적이니까
    //주소를 init할때 가져와서, 가져온 주소를 변수 상태로 저장
    //해서 해당 주소를 사용하면 될듯
    buildingName = widget.data['BuildingName'];
    _selectedFloorEndPoint = widget.selectedFloor; // 초기 층을 출발 층으로 설정
    imageUrl = getImageurl();
  }

  String getImageurl() {
    return "https://$apiUrl/mask/${buildingName}_${_selectedFloorEndPoint!.toString().padLeft(2, '0').replaceAll("-", "B")}";
  }

  Future<String> findWay(data) async {
    setState(() {
      isLoading = true; //로딩 시작
    });
    log("길찾기 시작");
    var apilink = Uri.parse("https://$apiUrl/findway");
    http.Response response = await http.post(apilink,
        headers: {
          'Content-Type': 'application/json',
        },
        body: data);
    log(response.body);
    setState(() {
      isLoading = false; //로딩 완료
    });
    return response.body; // API에서 종료메시지 전달
  }

  @override
  Widget build(BuildContext context) {
    log(widget.data.toString());
    int? basementFloor = widget.data['Basement'];
    int floors = widget.data['Floors'];

    final selectedFloor = widget.selectedFloor;
    final selectedLocation = widget.selectedLocation;
    log(selectedLocation.toString());
    //전달받은 출발한 층과 장소
    log(selectedFloor.toString());
    return Stack(
      children: [
        Scaffold(
          body: Column(children: <Widget>[
            Row(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 10, top: 15),
                  child: Text(
                    "$buildingName\n실내\n길 찾기.",
                    style: const TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 49, 49, 49),
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.only(left: 15, right: 15),
              child: DropdownSearch<String>(
                popupProps: PopupProps.menu(
                  showSelectedItems: true,
                  disabledItemFn: (String s) => s.startsWith('I'),
                ),
                items: createFloorList(basementFloor, floors),
                dropdownDecoratorProps: const DropDownDecoratorProps(
                  dropdownSearchDecoration: InputDecoration(
                      labelText: "층",
                      hintText: "층 선택",
                      labelStyle:
                          TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                      hintStyle:
                          TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                ),
                onChanged: (value) async {
                  value = value?.replaceAll('B', '-');
                  _selectedFloorEndPoint = int.parse(value!);
                  _showLocationDropdown = true;
                  imageUrl = getImageurl();
                  DocumentSnapshot storeDocument = await FirebaseFirestore
                      .instance
                      .collection('buildings')
                      .doc(widget.documentId)
                      .collection('stores')
                      .doc(
                          '${widget.documentId}_${_selectedFloorEndPoint!.toString().padLeft(2, "0").replaceAll("-", "B")}')
                      .get();
                  var tempData = storeDocument.data()
                      as Map<String, dynamic>; // 데이터를 Map 형태로 받음
                  _storeNames = tempData.entries.map((entry) {
                    return Store("${entry.key}: ${entry.value}", entry.key);
                  }).toList();
                  setState(() {});
                },
              ),
            ),
            if (_showLocationDropdown)
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15),
                child: CustomDropdown<Store>.search(
                  hintText: '도착지 선택',
                  items: _storeNames,
                  excludeSelected: false,
                  onChanged: (value) {
                    log('changing value to: ${value.id}');
                    _selectedLocationEndPoint = int.parse(value.id);
                    setState(() {});
                  },
                ),
              ),
            // 여기에 계단, 엘리베이터 입력받는거 필요함
            if (_selectedLocationEndPoint != null)
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15),
                child: DropdownSearch<String>(
                  popupProps: PopupProps.menu(
                    showSelectedItems: true,
                    disabledItemFn: (String s) => s.startsWith('I'),
                  ),
                  items: const ["계단", "엘리베이터"],
                  dropdownDecoratorProps: const DropDownDecoratorProps(
                    dropdownSearchDecoration: InputDecoration(
                        labelText: "이동 수단 선택",
                        hintText: "이동 수단 선택",
                        labelStyle: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                        hintStyle: TextStyle(
                            fontSize: 15, fontWeight: FontWeight.bold)),
                  ),
                  onChanged: (value) {
                    setState(() {
                      if (value == "계단") {
                        _selectedTransportMethod = 0;
                      } else {
                        _selectedTransportMethod = 1;
                      }
                    });
                  },
                ),
              ),
            if (_selectedTransportMethod != null)
              Padding(
                padding: const EdgeInsets.only(left: 15, top: 15, right: 15),
                child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      foregroundColor: Colors.white,
                      minimumSize: const Size.fromHeight(50),
                      backgroundColor:
                          const Color.fromARGB(255, 49, 49, 49), // 버튼의 텍스트 색상
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10), // 버튼의 모서리를 둥글게
                      ),
                    ),
                    onPressed: () async {
                      clearCache();
                      if (_selectedFloorEndPoint != null &&
                          _selectedLocationEndPoint != null) {
                        // 임시값..
                        var data = json.encode({
                          "building_name": buildingName,
                          "startFloor": selectedFloor,
                          "startId": selectedLocation,
                          "endFloor": _selectedFloorEndPoint,
                          "endId": _selectedLocationEndPoint,
                          "elev": _selectedTransportMethod,
                        });
                        // 길찾기 실행중
                        // ignore: unused_local_variable
                        var x = await findWay(data);
                        // 종료
                        // ignore: use_build_context_synchronously
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => DirectionGuidance(
                              startFloor: selectedFloor,
                              endFloor: _selectedFloorEndPoint!,
                              data: widget.data,
                            ),
                          ),
                        );
                      }
                    },
                    child: Text(isLoading ? "길 찾기 실행 중 . . ." : "도착지 선택 완료")),
              ),
            const Divider(
              color: Color.fromARGB(255, 170, 170, 170),
            ),
            Expanded(
              child: imageUrl.isEmpty
                  ? const Center(child: CircularProgressIndicator())
                  : InteractiveViewer(
                      maxScale: 5.0,
                      minScale: 0.01,
                      child: SizedBox(
                        width: double.infinity,
                        height: double.infinity,
                        child: Image(
                            image: NetworkImage(imageUrl), fit: BoxFit.fill),
                      ),
                    ),
            ),
          ]),
        ),
        if (isLoading)
          Container(
            color: Colors.black.withOpacity(0.5), // 투명한 검정색 배경
            child: const Center(child: CircularProgressIndicator()),
          ),
      ],
    );
  }

  List<String> createFloorList(int? basementFloor, int floors) {
    List<String> floorList = [];
    if (basementFloor != null) {
      for (int i = basementFloor; i >= 1; i--) {
        floorList.add("B$i");
      }
    }
    for (int i = 1; i <= floors; i++) {
      floorList.add("$i");
    }
    return floorList;
  }
}
