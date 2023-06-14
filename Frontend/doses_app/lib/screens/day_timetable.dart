import 'package:flutter/material.dart';
// import 'package:provider/provider.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:intl/intl.dart';

import '../widgets/calendar_utils.dart';
import './hour_timetable.dart';

class DosesDayCalendarPage extends StatefulWidget {
  const DosesDayCalendarPage({
    super.key,
  });

  @override
  State<DosesDayCalendarPage> createState() => _DosesDayCalendarPageState();
}

class _DosesDayCalendarPageState extends State<DosesDayCalendarPage> {
  late final ValueNotifier<List<Event>> _selectedEvents;
  CalendarFormat _calendarFormat = CalendarFormat.week;
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  

  @override
  void initState() {
    super.initState();
    _selectedDay = _focusedDay;
    _selectedEvents = ValueNotifier(_getEventsForDay(_selectedDay!));
  }

  @override
  void dispose() {
    _selectedEvents.dispose();
    super.dispose();
  }

  List<Event> _getEventsForDay(DateTime day) {
    // Implementation example
    return kEvents[day] ?? [];
  }

  @override
  Widget build(BuildContext context) {
    // var mainAppState = Provider.of<MainAppState>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Doses reminder'),
      ),
      body: Center(
        child: Column(
          children: [
            TableCalendar<Event>(
              calendarFormat: _calendarFormat,
              locale: "en_US",
              firstDay: kFirstDay,
              headerStyle: const HeaderStyle(
                formatButtonVisible: false,
              ),
              lastDay: kLastDay,
              focusedDay: _focusedDay,
              eventLoader: _getEventsForDay,
              selectedDayPredicate: (day) {
                return isSameDay(_selectedDay, day);
              },
              onDaySelected: _onDaySelected,
              onFormatChanged: (format) {
                if (_calendarFormat != format) {
                  // Call `setState()` when updating calendar format
                  setState(() {
                    _calendarFormat = format;
                  });
                }
              },
              onPageChanged: (focusedDay) {
                // No need to call `setState()` here
                _focusedDay = focusedDay;
              },
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(DateFormat("HH:mm").format(_selectedDay ?? DateTime.now())),
                IconButton(
                  icon: const Icon(Icons.today),
                  onPressed: () {
                    _onDaySelected(DateTime.now(), DateTime.now());
                  },
                ),
              ],
            ),
            const SizedBox(height: 8.0),
            Expanded(
              child: ValueListenableBuilder<List<Event>>(
                valueListenable: _selectedEvents,
                builder: (context, value, _) {
                  return ListView.builder(
                    itemCount: value.length,
                    itemBuilder: (context, index) {
                      // final item = droppers[index];
                      return Container(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 12.0,
                          vertical: 4.0,
                        ),
                        decoration: BoxDecoration(
                          border: Border.all(), 
                          borderRadius: BorderRadius.circular(12.0),
                        ),
                        child: ListTile(
                          onTap: () {
                            // print('${value[index]}');
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const DosesHourTimetablePage(),
                              ),
                            );
                          },
                          title: Text('${value[index]}'),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _onDaySelected(selectedDay, focusedDay) {
    if (!isSameDay(_selectedDay, selectedDay)) {
      // Call `setState()` when updating the selected day
      setState(() {
        _selectedDay = selectedDay;
        _focusedDay = focusedDay;
        _selectedEvents.value = _getEventsForDay(selectedDay);
      });
    }
  }
}

class MainAppState extends ChangeNotifier {
  // var dateSelected = CalendarDatePicker();
}