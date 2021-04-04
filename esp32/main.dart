/**
 * Copyright 2019, Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'login.dart';
import 'devices.dart';
import 'register.dart';
// Import the firebase_core plugin
// ignore: import_of_legacy_library_into_null_safe
import "package:firebase_analytics/firebase_analytics.dart";
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_remote_config/firebase_remote_config.dart';

RemoteConfig remoteConfig;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  await Firebase.initializeApp();
  RemoteConfig remoteConfig = RemoteConfig.instance;

  runApp(DeviceManagerApp());
}

class DeviceManagerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: remoteConfig.getString('_appTitle'),
      // Start the app at the login screen
      initialRoute: '/',
      routes: {
        '/': (context) =>
            LoginScreen(title: remoteConfig.getString('_LoginScreenTitle')),
        '/devices': (context) => DeviceListScreen(
            title: remoteConfig.getString('_DeviceListScreenTitle')),
        '/register': (context) => RegisterDeviceScreen(
            title: remoteConfig.getString('_RegisterDeviceScreenTitle')),
      },
    );
  }
}
