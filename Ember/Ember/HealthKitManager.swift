//
//  HealthKitManager.swift
//  Ember
//
//  Created by Khush Bakht Rehman on 17/06/2023.
//

import Foundation
import HealthKit

class HealthKitManager {
    static let healthStore = HKHealthStore()
    
    static func requestAuthorization() {
        guard HKHealthStore.isHealthDataAvailable() else {
            return
        }
        
        let allTypes = Set([HKObjectType.quantityType(forIdentifier: .activeEnergyBurned)!,
                            HKObjectType.quantityType(forIdentifier: .stepCount)!,
                            HKObjectType.quantityType(forIdentifier: .heartRate)!,
                            HKObjectType.quantityType(forIdentifier: .bodyMassIndex)!,
                            HKObjectType.quantityType(forIdentifier: .height)!,
                            HKObjectType.quantityType(forIdentifier: .bodyMass)!])
        
        healthStore.requestAuthorization(toShare: allTypes, read: allTypes) { (success, error) in
            if success {
                print("Authorization complete")
            } else if let error = error {
                print("Authorization error: \(error.localizedDescription)")
            }
        }
    }
}
