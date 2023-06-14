import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:doses_app/models/api_constants.dart';
import 'package:doses_app/models/dropper.dart';

//Reference: https://blog.codemagic.io/rest-api-in-flutter/

class ApiService {
  Future<List<Dropper>?> getDroppers() async {
    try {
      final url = Uri.parse(ApiConstants.baseUrl + ApiConstants.droppersEndpoint);
      var response = await http.get(url);
      List<Dropper> modelDroppers = List<Dropper>.empty();
      if (response.statusCode == 200) {
        modelDroppers = droppersFromJson(response.body);
        return modelDroppers;
      }
      return modelDroppers;
    } catch (e) {
      log(e.toString());
    }
    return null;
  }
}