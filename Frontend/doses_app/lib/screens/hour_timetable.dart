import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:doses_app/models/dropper.dart';
import 'package:doses_app/models/api_service.dart';
import 'dart:io' show Platform;


class DosesHourTimetablePage extends StatefulWidget {
  const DosesHourTimetablePage({
    super.key,
  });

  @override
  State<DosesHourTimetablePage> createState() => _DosesHourTimetablePageState();
}

class _DosesHourTimetablePageState extends State<DosesHourTimetablePage> {
  late List<Dropper>? _droppersModel = [];
  @override
  void initState() {
    super.initState();
    _getData();
  }

  void _getData() async {
    _droppersModel = (await ApiService().getDroppers())!;
    Future.delayed(const Duration(seconds: 1)).then((value) => setState(() {}));
  }

  @override
  Widget build(BuildContext context) {

    // Group droppers by a specific property in a map
    // var coldChain= groupBy(_droppersModel!, (Dropper dropper) => dropper.coldChain);

    // Choose the right progress indicator according to the platform
    Widget getIndicatorWidget(TargetPlatform platform) {
      switch (platform) {
        case TargetPlatform.iOS:
        case TargetPlatform.macOS:
          return const CupertinoActivityIndicator();
        case TargetPlatform.android:
        case TargetPlatform.fuchsia:
        case TargetPlatform.linux:
        case TargetPlatform.windows:
        default:
          return const CircularProgressIndicator();
      }
    }

    return Scaffold(
      appBar: AppBar(title: const Text("Doses")),
      body: _droppersModel == null || _droppersModel!.isEmpty
          ? Center(
              child: getIndicatorWidget(defaultTargetPlatform),
            )
          : ListView.builder(
              itemCount: _droppersModel!.length,
              itemBuilder: (context, index) {
                Text description;
                if(_droppersModel![index].description != null) {
                  description = Text(_droppersModel![index].description);
                }
                else {
                  description = const Text("Sin descripción");
                }
                return Card(
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Text(_droppersModel![index].placeToApply != null ? _droppersModel![index].placeToApply! : "Random"),
                          Text(_droppersModel![index].name),
                        ],
                      ),
                      const SizedBox(
                        height: 20.0,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          // DateTime(_dropperModel![index].dateExpiration),
                          description,
                        ],
                      ),
                    ],
                  ),
                );
              },
            ),
    );
  }
}