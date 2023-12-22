import 'package:animated_custom_dropdown/custom_dropdown.dart';

class Store with CustomDropdownListFilter {
  final String name;
  final String id;
  const Store(this.name, this.id);

  @override
  String toString() {
    return name;
  }

  @override
  bool filter(String query) {
    return name.toLowerCase().contains(query.toLowerCase());
  }
}
