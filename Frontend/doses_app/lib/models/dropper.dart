// To parse this JSON data, do
//
//     final droppers = droppersFromJson(jsonString);

import 'dart:convert';

List<Dropper> droppersFromJson(String str) => List<Dropper>.from(json.decode(str).map((x) => Dropper.fromJson(x)));

String droppersToJson(List<Dropper> data) => json.encode(List<dynamic>.from(data.map((x) => x.toJson())));

class Dropper {
    String id;
    String name;
    String? code;
    dynamic description;
    bool? coldChain;
    int? volume;
    DateTime? dateExpiration;
    String? color;
    bool? opened;
    String? placeToApply;

    Dropper({
        required this.id,
        required this.name,
        this.code,
        this.description,
        this.coldChain,
        this.volume,
        this.dateExpiration,
        this.color,
        this.opened,
        this.placeToApply,
    });

    factory Dropper.fromJson(Map<String, dynamic> json) => Dropper(
        id: json["id"],
        name: json["name"],
        code: json["code"],
        description: json["description"],
        coldChain: json["cold_chain"],
        volume: json["volume"],
        dateExpiration: DateTime.parse(json["date_expiration"]),
        color: json["color"],
        opened: json["opened"],
        placeToApply: json["placeToApply"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "name": name,
        "code": code,
        "description": description,
        "cold_chain": coldChain,
        "volume": volume,
        // "date_expiration": "${dateExpiration.year.toString().padLeft(4, '0')}-${dateExpiration.month.toString().padLeft(2, '0')}-${dateExpiration.day.toString().padLeft(2, '0')}",
        "color": color,
        "opened": opened,
        "placeToApply": placeToApply,
    };
}

// List droppers = [
//   {
//     "id": "6417b00c36a1f48e085739f6",
//     "name": "Clorhexidina",
//     "code": "2904282",
//     "description": null,
//     "cold_chain": false,
//     "volume": 10,
//     "date_expiration": "2023-05-07",
//     "color": "white",
//     "opened": true
//   },
//   {
//     "id": "6417e646f1a687ad69c5ac7d",
//     "name": "PHMB",
//     "code": "904281",
//     "description": "Para quistes de Acanthamoeba",
//     "cold_chain": false,
//     "volume": 10,
//     "date_expiration": "2023-05-07",
//     "color": "white",
//     "opened": true
//   },
//   {
//     "id": "641c8fe95231d58846b64dc9",
//     "date_expiration": "2023-04-22",
//     "name": "Voriconazol",
//     "code": "2904280",
//     "description": "Antimicótico",
//     "cold_chain": false,
//     "volume": 5,
//     "color": "white",
//     "opened": true
//   },
//   {
//     "id": "641ca63dee673e7e8d9d6ec9",
//     "date_expiration": "2023-04-08",
//     "name": "Ciclosporina",
//     "code": "2905086",
//     "description": "Modulador inmunológico",
//     "cold_chain": false,
//     "volume": 5,
//     "color": "white",
//     "opened": true
//   },
//   {
//     "id": "641cb02c3b6bb5ddbc9be085",
//     "date_expiration": "2023-09-11",
//     "name": "Artelac - Rebalance",
//     "code": null,
//     "description": "Lágrima artificial",
//     "cold_chain": null,
//     "volume": 10,
//     "color": null,
//     "opened": true
//   },
//   {
//     "id": "64206bc9bf66f7ea177404e7",
//     "date_expiration": "2023-04-19",
//     "name": "Anfotericina",
//     "code": "2906258",
//     "description": null,
//     "cold_chain": true,
//     "volume": 10,
//     "color": "white",
//     "opened": true
//   },
//   {
//     "id": "642dcc39b6dc695736bbe2dd",
//     "date_expiration": "1024-04-01",
//     "name": "Sedesterol",
//     "code": "4018801904",
//     "description": "Corticoide - Dexametasona 21 fosfato de sodio 0.1%",
//     "cold_chain": false,
//     "volume": 5,
//     "color": "white",
//     "opened": true
//   }
// ];
