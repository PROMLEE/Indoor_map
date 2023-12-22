import 'dart:developer';

import 'api_key.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:dropdown_search/dropdown_search.dart';
import 'package:flutter/material.dart';
import 'package:navermaptest01/visitor_choose_endpoint.dart';
import 'package:animated_custom_dropdown/custom_dropdown.dart';
import 'searchbox.dart';

class ThirdScreen extends StatefulWidget {
  const ThirdScreen({required this.data, required this.documentId, Key? key})
      : super(key: key);
  final dynamic data; // 받을 데이터를 위한 변수 추가
  final String documentId;
  @override
  State<ThirdScreen> createState() => _ThirdScreenState();
}

class _ThirdScreenState extends State<ThirdScreen> {
  //imageUrl을 초기값을 설정해줘야 예외 발생안됨 빈문자열 만듬
  String imageUrl = '';
  Map<String, dynamic> tempData = {};
  int? _selectedFloor;
  int? _selectedLocation = 0;
  bool _showLocationDropdown = false;
  late String buildingName;
  List<Store> list = [];
  @override
  void initState() {
    super.initState();
    //층, 출발지 선택을 할때마다 이미지를 가져오는 문제 찾음
    //문제라기보단 비효율적이니까
    //주소를 init할때 가져와서, 가져온 주소를 변수 상태로 저장
    //해서 해당 주소를 사용하면 될듯
    buildingName = widget.data['BuildingName'];
    _selectedFloor = 1; //층 선택하기전에 기본 이미지
    imageUrl = getImageurl();
    //건물이름으로 이미지 접근해야 하니까 위젯이 생성되기전에 초기화
  }

  String getImageurl() {
    log("${buildingName}_$_selectedFloor");
    return "https://$apiUrl/mask/${buildingName}_${_selectedFloor.toString().padLeft(2, '0').replaceAll("-", "B")}";
  }

  @override
  Widget build(BuildContext context) {
    int? basementFloor = widget.data['Basement'];
    int floors = widget.data['Floors'];
    return Scaffold(
      body: Column(
        children: <Widget>[
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
                _selectedFloor = int.parse(value!);
                _showLocationDropdown = true;
                imageUrl = getImageurl();
                DocumentSnapshot storeDocument = await FirebaseFirestore
                    .instance
                    .collection('buildings')
                    .doc(widget.documentId)
                    .collection('stores')
                    .doc(
                        '${widget.documentId}_${_selectedFloor.toString().padLeft(2, '0').replaceAll("-", "B")}')
                    .get();
                tempData = storeDocument.data()
                    as Map<String, dynamic>; //데이터를 Map 형태로 받음
                list = tempData.entries.map((entry) {
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
                hintText: '출발지 선택',
                items: list,
                excludeSelected: false,
                onChanged: (value) {
                  log('changing value to: ${value.id}');
                  _selectedLocation = int.parse(value.id);
                  log(_selectedLocation.toString());
                  setState(() {});
                },
              ),
            ),
          if (_selectedLocation != 0)
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
                  onPressed: () {
                    if (_selectedFloor != null) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => VisitorChooseEndPoint(
                            selectedFloor: _selectedFloor!,
                            selectedLocation: _selectedLocation!,
                            data: widget.data,
                            documentId: widget.documentId,
                          ),
                        ),
                      );
                    }
                  },
                  child: const Text("출발지 선택 완료")),
            ),
          const Divider(
            color: Color.fromARGB(255, 170, 170, 170),
          ),
          //이미지 위젯
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
                        image: NetworkImage(imageUrl),
                        fit: BoxFit.fill,
                      ),
                    ),
                  ),
          ),
        ],
      ),
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
