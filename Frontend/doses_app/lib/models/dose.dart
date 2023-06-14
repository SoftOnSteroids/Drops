// To parse this JSON data, do
//
//     final dose = dosesFromJson(jsonString);

import 'dart:convert';

List<Dose> dosesFromJson(String str) => List<Dose>.from(json.decode(str).map((x) => Dose.fromJson(x)));

String dosesToJson(List<Dose> data) => json.encode(List<dynamic>.from(data.map((x) => x.toJson())));

class Dose {
    String id;
    String dropperId;
    String? applicationTime;
    DateTime dateStart;
    int timeIsolation;
    int timeSeparationFrequence;
    String placeToApply;
    dynamic dateEnd;
    dynamic dayStartTime;
    dynamic dayEndTime;
    int frequenceInDay;
    int priority;

    Dose({
        required this.id,
        required this.dropperId,
        this.applicationTime,
        required this.dateStart,
        required this.timeIsolation,
        required this.timeSeparationFrequence,
        required this.placeToApply,
        this.dateEnd,
        this.dayStartTime,
        this.dayEndTime,
        required this.frequenceInDay,
        required this.priority,
    });

    factory Dose.fromJson(Map<String, dynamic> json) => Dose(
        id: json["id"],
        dropperId: json["dropper_id"],
        applicationTime: json["application_time"],
        dateStart: DateTime.parse(json["date_start"]),
        timeIsolation: json["time_isolation"],
        timeSeparationFrequence: json["time_separation_frequence"],
        placeToApply: json["place_to_apply"],
        dateEnd: json["date_end"],
        dayStartTime: json["day_start_time"],
        dayEndTime: json["day_end_time"],
        frequenceInDay: json["frequence_in_day"],
        priority: json["priority"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "dropper_id": dropperId,
        "application_time": applicationTime,
        "date_start": "${dateStart.year.toString().padLeft(4, '0')}-${dateStart.month.toString().padLeft(2, '0')}-${dateStart.day.toString().padLeft(2, '0')}",
        "time_isolation": timeIsolation,
        "time_separation_frequence": timeSeparationFrequence,
        "place_to_apply": placeToApply,
        "date_end": dateEnd,
        "day_start_time": dayStartTime,
        "day_end_time": dayEndTime,
        "frequence_in_day": frequenceInDay,
        "priority": priority,
    };
}
