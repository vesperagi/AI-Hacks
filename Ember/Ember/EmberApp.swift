//
//  EmberApp.swift
//  Ember
//
//  Created by Khush Bakht Rehman on 17/06/2023.
//

import SwiftUI
import Firebase

@main
struct EmberApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
  func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
    FirebaseApp.configure()
      
    HealthKitManager.requestAuthorization()

    return true
  }
}
