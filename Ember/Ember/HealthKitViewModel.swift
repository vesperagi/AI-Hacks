//
//  HealthKitViewModel.swift
//  Ember
//
//  Created by Khush Bakht Rehman on 17/06/2023.
//

import Foundation
import HealthKit

import Firebase

let db = Firestore.firestore()

class HealthKitViewModel: ObservableObject {
    
    private var healthStore: HKHealthStore?
    
    init() {

        if HKHealthStore.isHealthDataAvailable() {
            healthStore = HKHealthStore()
        }
    }
    
    func requestAuthorization() {
        let readDataTypes: Set<HKSampleType> = [
            
            // Exercise
            HKSampleType.quantityType(forIdentifier: .stepCount)!,
            HKSampleType.quantityType(forIdentifier: .distanceWalkingRunning)!,
            HKSampleType.quantityType(forIdentifier: .distanceCycling)!,
            HKSampleType.quantityType(forIdentifier: .pushCount)!,
            HKSampleType.quantityType(forIdentifier: .distanceWheelchair)!,
            HKSampleType.quantityType(forIdentifier: .distanceSwimming)!,
            // Body Measurements
            HKSampleType.quantityType(forIdentifier: .bodyMassIndex)!,
            HKSampleType.quantityType(forIdentifier: .bodyFatPercentage)!,
            HKSampleType.quantityType(forIdentifier: .height)!,
            HKSampleType.quantityType(forIdentifier: .bodyMass)!,
            HKSampleType.quantityType(forIdentifier: .leanBodyMass)!,
            // Reproductive Health
            HKSampleType.quantityType(forIdentifier: .basalBodyTemperature)!,
            // Hearing
            HKSampleType.quantityType(forIdentifier: .environmentalAudioExposure)!,
            HKSampleType.quantityType(forIdentifier: .headphoneAudioExposure)!,
            // Vital Signs
            HKSampleType.quantityType(forIdentifier: .heartRate)!,
            // More exercise metrics
            HKSampleType.quantityType(forIdentifier: .basalEnergyBurned)!,
            HKSampleType.quantityType(forIdentifier: .activeEnergyBurned)!,
            HKSampleType.quantityType(forIdentifier: .flightsClimbed)!,
            HKSampleType.quantityType(forIdentifier: .vo2Max)!,
            // More body measurements
            HKSampleType.quantityType(forIdentifier: .bodyFatPercentage)!,
            HKSampleType.quantityType(forIdentifier: .waistCircumference)!,
            // More vital signs
            HKSampleType.quantityType(forIdentifier: .heartRateRecoveryOneMinute)!,
            HKSampleType.quantityType(forIdentifier: .respiratoryRate)!,
            // Lab and test results
            HKSampleType.quantityType(forIdentifier: .bloodGlucose)!,
            HKSampleType.quantityType(forIdentifier: .electrodermalActivity)!,
            HKSampleType.quantityType(forIdentifier: .forcedExpiratoryVolume1)!,
            HKSampleType.quantityType(forIdentifier: .forcedVitalCapacity)!,
            HKSampleType.quantityType(forIdentifier: .inhalerUsage)!,
            HKSampleType.quantityType(forIdentifier: .insulinDelivery)!,
            HKSampleType.quantityType(forIdentifier: .numberOfTimesFallen)!,
            HKSampleType.quantityType(forIdentifier: .peakExpiratoryFlowRate)!,
            HKSampleType.quantityType(forIdentifier: .peripheralPerfusionIndex)!,
            // And so on... You can continue to add all types as shown above
            // Nutrition
            HKSampleType.quantityType(forIdentifier: .dietaryWater)!,
            HKSampleType.quantityType(forIdentifier: .dietaryBiotin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCaffeine)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCalcium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCarbohydrates)!,
            HKSampleType.quantityType(forIdentifier: .dietaryChloride)!,
            HKSampleType.quantityType(forIdentifier: .dietaryChromium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCopper)!,
            HKSampleType.quantityType(forIdentifier: .dietaryEnergyConsumed)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatMonounsaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatPolyunsaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatSaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatTotal)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFiber)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFolate)!,
            HKSampleType.quantityType(forIdentifier: .dietaryIodine)!,
            HKSampleType.quantityType(forIdentifier: .dietaryIron)!,
            HKSampleType.quantityType(forIdentifier: .dietaryMagnesium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryManganese)!,
            HKSampleType.quantityType(forIdentifier: .dietaryMolybdenum)!,
            HKSampleType.quantityType(forIdentifier: .dietaryNiacin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPantothenicAcid)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPhosphorus)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPotassium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryProtein)!,
            HKSampleType.quantityType(forIdentifier: .dietaryRiboflavin)!,
            HKSampleType.quantityType(forIdentifier: .dietarySelenium)!,
            HKSampleType.quantityType(forIdentifier: .dietarySodium)!,
            HKSampleType.quantityType(forIdentifier: .dietarySugar)!,
            HKSampleType.quantityType(forIdentifier: .dietaryThiamin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminA)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminB12)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminB6)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminC)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminD)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminE)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminK)!,
            HKSampleType.quantityType(forIdentifier: .dietaryZinc)!,
            
            // Mobility
            HKSampleType.quantityType(forIdentifier: .walkingSpeed)!,
            HKSampleType.quantityType(forIdentifier: .stairAscentSpeed)!,
            HKSampleType.quantityType(forIdentifier: .stairDescentSpeed)!,
            HKSampleType.quantityType(forIdentifier: .walkingDoubleSupportPercentage)!,
            HKSampleType.quantityType(forIdentifier: .sixMinuteWalkTestDistance)!,
            
            // UV Exposure
            HKSampleType.quantityType(forIdentifier: .uvExposure)!,
            
        ]
        
        let writeDataTypes: Set<HKSampleType> = [
            // Exercise
            HKSampleType.quantityType(forIdentifier: .stepCount)!,
            HKSampleType.quantityType(forIdentifier: .distanceWalkingRunning)!,
            HKSampleType.quantityType(forIdentifier: .distanceCycling)!,
            HKSampleType.quantityType(forIdentifier: .pushCount)!,
            HKSampleType.quantityType(forIdentifier: .distanceWheelchair)!,
            HKSampleType.quantityType(forIdentifier: .distanceSwimming)!,
            // Body Measurements
            HKSampleType.quantityType(forIdentifier: .bodyMassIndex)!,
            HKSampleType.quantityType(forIdentifier: .bodyFatPercentage)!,
            HKSampleType.quantityType(forIdentifier: .height)!,
            HKSampleType.quantityType(forIdentifier: .bodyMass)!,
            HKSampleType.quantityType(forIdentifier: .leanBodyMass)!,
            // Reproductive Health
            HKSampleType.quantityType(forIdentifier: .basalBodyTemperature)!,
            // Hearing
            HKSampleType.quantityType(forIdentifier: .environmentalAudioExposure)!,
            HKSampleType.quantityType(forIdentifier: .headphoneAudioExposure)!,
            // Vital Signs
            HKSampleType.quantityType(forIdentifier: .heartRate)!,
            // More exercise metrics
            HKSampleType.quantityType(forIdentifier: .basalEnergyBurned)!,
            HKSampleType.quantityType(forIdentifier: .activeEnergyBurned)!,
            HKSampleType.quantityType(forIdentifier: .flightsClimbed)!,
            HKSampleType.quantityType(forIdentifier: .vo2Max)!,
            // More body measurements
            HKSampleType.quantityType(forIdentifier: .bodyFatPercentage)!,
            HKSampleType.quantityType(forIdentifier: .waistCircumference)!,
            // More vital signs
            HKSampleType.quantityType(forIdentifier: .heartRateRecoveryOneMinute)!,
            HKSampleType.quantityType(forIdentifier: .respiratoryRate)!,
            // Lab and test results
            HKSampleType.quantityType(forIdentifier: .bloodGlucose)!,
            HKSampleType.quantityType(forIdentifier: .electrodermalActivity)!,
            HKSampleType.quantityType(forIdentifier: .forcedExpiratoryVolume1)!,
            HKSampleType.quantityType(forIdentifier: .forcedVitalCapacity)!,
            HKSampleType.quantityType(forIdentifier: .inhalerUsage)!,
            HKSampleType.quantityType(forIdentifier: .insulinDelivery)!,
            HKSampleType.quantityType(forIdentifier: .numberOfTimesFallen)!,
            HKSampleType.quantityType(forIdentifier: .peakExpiratoryFlowRate)!,
            HKSampleType.quantityType(forIdentifier: .peripheralPerfusionIndex)!,
            // And so on... You can continue to add all types as shown above
            // Nutrition
            HKSampleType.quantityType(forIdentifier: .dietaryWater)!,
            HKSampleType.quantityType(forIdentifier: .dietaryBiotin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCaffeine)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCalcium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCarbohydrates)!,
            HKSampleType.quantityType(forIdentifier: .dietaryChloride)!,
            HKSampleType.quantityType(forIdentifier: .dietaryChromium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryCopper)!,
            HKSampleType.quantityType(forIdentifier: .dietaryEnergyConsumed)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatMonounsaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatPolyunsaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatSaturated)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFatTotal)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFiber)!,
            HKSampleType.quantityType(forIdentifier: .dietaryFolate)!,
            HKSampleType.quantityType(forIdentifier: .dietaryIodine)!,
            HKSampleType.quantityType(forIdentifier: .dietaryIron)!,
            HKSampleType.quantityType(forIdentifier: .dietaryMagnesium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryManganese)!,
            HKSampleType.quantityType(forIdentifier: .dietaryMolybdenum)!,
            HKSampleType.quantityType(forIdentifier: .dietaryNiacin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPantothenicAcid)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPhosphorus)!,
            HKSampleType.quantityType(forIdentifier: .dietaryPotassium)!,
            HKSampleType.quantityType(forIdentifier: .dietaryProtein)!,
            HKSampleType.quantityType(forIdentifier: .dietaryRiboflavin)!,
            HKSampleType.quantityType(forIdentifier: .dietarySelenium)!,
            HKSampleType.quantityType(forIdentifier: .dietarySodium)!,
            HKSampleType.quantityType(forIdentifier: .dietarySugar)!,
            HKSampleType.quantityType(forIdentifier: .dietaryThiamin)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminA)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminB12)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminB6)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminC)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminD)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminE)!,
            HKSampleType.quantityType(forIdentifier: .dietaryVitaminK)!,
            HKSampleType.quantityType(forIdentifier: .dietaryZinc)!,
            
            // Mobility
            HKSampleType.quantityType(forIdentifier: .walkingSpeed)!,
            HKSampleType.quantityType(forIdentifier: .stairAscentSpeed)!,
            HKSampleType.quantityType(forIdentifier: .stairDescentSpeed)!,
            HKSampleType.quantityType(forIdentifier: .walkingDoubleSupportPercentage)!,
            HKSampleType.quantityType(forIdentifier: .sixMinuteWalkTestDistance)!,
            
            // UV Exposure
            HKSampleType.quantityType(forIdentifier: .uvExposure)!,
        ]
        
        
        healthStore?.requestAuthorization(toShare: writeDataTypes, read: readDataTypes) { (success, error) in
            if let error = error {
                print("Error requesting authorization: \(error)")
            } else {
                print("Authorization request succeeded")
                DispatchQueue.main.async {
                    self.fetchData(for: .stepCount)
                    self.fetchData(for: .distanceWalkingRunning)
                    self.fetchData(for: .distanceCycling)
                    self.fetchData(for: .pushCount)
                    self.fetchData(for: .distanceWheelchair)
                    self.fetchData(for: .distanceSwimming)
                    self.fetchData(for: .bodyMassIndex)
                    self.fetchData(for: .bodyFatPercentage)
                    self.fetchData(for: .height)
                    self.fetchData(for: .bodyMass)
                    self.fetchData(for: .leanBodyMass)
                    self.fetchData(for: .basalBodyTemperature)
                    self.fetchData(for: .environmentalAudioExposure)
                    self.fetchData(for: .headphoneAudioExposure)
                    self.fetchData(for: .heartRate)
                    self.fetchData(for: .basalEnergyBurned)
                    self.fetchData(for: .activeEnergyBurned)
                    self.fetchData(for: .flightsClimbed)
                    self.fetchData(for: .vo2Max)
                    self.fetchData(for: .waistCircumference)
                    self.fetchData(for: .heartRateRecoveryOneMinute)
                    self.fetchData(for: .respiratoryRate)
                    self.fetchData(for: .bloodGlucose)
                    self.fetchData(for: .electrodermalActivity)
                    self.fetchData(for: .forcedExpiratoryVolume1)
                    self.fetchData(for: .forcedVitalCapacity)
                    self.fetchData(for: .inhalerUsage)
                    self.fetchData(for: .insulinDelivery)
                    self.fetchData(for: .numberOfTimesFallen)
                    self.fetchData(for: .peakExpiratoryFlowRate)
                    self.fetchData(for: .peripheralPerfusionIndex)
                    self.fetchData(for: .dietaryWater)
                    self.fetchData(for: .dietaryBiotin)
                    self.fetchData(for: .dietaryCaffeine)
                    self.fetchData(for: .dietaryCalcium)
                    self.fetchData(for: .dietaryCarbohydrates)
                    self.fetchData(for: .dietaryChloride)
                    self.fetchData(for: .dietaryChromium)
                    self.fetchData(for: .dietaryCopper)
                    self.fetchData(for: .dietaryEnergyConsumed)
                    self.fetchData(for: .dietaryFatMonounsaturated)
                    self.fetchData(for: .dietaryFatPolyunsaturated)
                    self.fetchData(for: .dietaryFatSaturated)
                    self.fetchData(for: .dietaryFatTotal)
                    self.fetchData(for: .dietaryFiber)
                    self.fetchData(for: .dietaryFolate)
                    self.fetchData(for: .dietaryIodine)
                    self.fetchData(for: .dietaryIron)
                    self.fetchData(for: .dietaryMagnesium)
                    self.fetchData(for: .dietaryManganese)
                    self.fetchData(for: .dietaryMolybdenum)
                    self.fetchData(for: .dietaryNiacin)
                    self.fetchData(for: .dietaryPantothenicAcid)
                    self.fetchData(for: .dietaryPhosphorus)
                    self.fetchData(for: .dietaryPotassium)
                    self.fetchData(for: .dietaryProtein)
                    self.fetchData(for: .dietaryRiboflavin)
                    self.fetchData(for: .dietarySelenium)
                    self.fetchData(for: .dietarySodium)
                    self.fetchData(for: .dietarySugar)
                    self.fetchData(for: .dietaryThiamin)
                    self.fetchData(for: .dietaryVitaminA)
                    self.fetchData(for: .dietaryVitaminB12)
                    self.fetchData(for: .dietaryVitaminB6)
                    self.fetchData(for: .dietaryVitaminC)
                    self.fetchData(for: .dietaryVitaminD)
                    self.fetchData(for: .dietaryVitaminE)
                    self.fetchData(for: .dietaryVitaminK)
                    self.fetchData(for: .dietaryZinc)
                    self.fetchData(for: .walkingSpeed)
                    self.fetchData(for: .stairAscentSpeed)
                    self.fetchData(for: .stairDescentSpeed)
                    self.fetchData(for: .walkingDoubleSupportPercentage)
                    self.fetchData(for: .sixMinuteWalkTestDistance)
                    self.fetchData(for: .uvExposure)
                    
                    
                }
            }
        }
    }
    
    //    func fetchData() {
    //        let sampleType = HKSampleType.quantityType(forIdentifier: .stepCount)!
    //        let query = HKSampleQuery(sampleType: sampleType, predicate: nil, limit: 0, sortDescriptors: nil) { (query, samples, error) in
    //            if let error = error {
    //                print("Error fetching data: \(error)")
    //                return
    //            }
    //
    //            if let samples = samples as? [HKQuantitySample] {
    //                for sample in samples {
    //                    print("Steps: \(sample.quantity.doubleValue(for: .count()))")
    //                }
    //            }
    //        }
    //
    //        healthStore?.execute(query)
    //    }
    
    enum HealthDataType {
        case stepCount, distanceWalkingRunning, distanceCycling, pushCount, distanceWheelchair,
             distanceSwimming, bodyMassIndex, bodyFatPercentage, height, bodyMass, leanBodyMass, basalBodyTemperature,
             environmentalAudioExposure, headphoneAudioExposure, heartRate, basalEnergyBurned, activeEnergyBurned, flightsClimbed,
             vo2Max, waistCircumference,
             heartRateRecoveryOneMinute, respiratoryRate,
             bloodGlucose, electrodermalActivity, forcedExpiratoryVolume1, forcedVitalCapacity, inhalerUsage, insulinDelivery,
             numberOfTimesFallen, peakExpiratoryFlowRate, peripheralPerfusionIndex, dietaryWater, dietaryBiotin, dietaryCaffeine,
             dietaryCalcium, dietaryCarbohydrates, dietaryChloride, dietaryChromium, dietaryCopper, dietaryEnergyConsumed,
             dietaryFatMonounsaturated, dietaryFatPolyunsaturated, dietaryFatSaturated, dietaryFatTotal, dietaryFiber, dietaryFolate,
             dietaryIodine, dietaryIron, dietaryMagnesium, dietaryManganese, dietaryMolybdenum, dietaryNiacin, dietaryPantothenicAcid,
             dietaryPhosphorus, dietaryPotassium, dietaryProtein, dietaryRiboflavin, dietarySelenium, dietarySodium, dietarySugar,
             dietaryThiamin, dietaryVitaminA, dietaryVitaminB12, dietaryVitaminB6, dietaryVitaminC, dietaryVitaminD, dietaryVitaminE,
             dietaryVitaminK, dietaryZinc, walkingSpeed, stairAscentSpeed, stairDescentSpeed, walkingDoubleSupportPercentage,
             sixMinuteWalkTestDistance, uvExposure
    }
    
    func fetchAllData() {
        let allTypes: [HealthDataType] = [.stepCount, .distanceWalkingRunning, .distanceCycling, .pushCount, .distanceWheelchair,
                                          .distanceSwimming, .bodyMassIndex, .bodyFatPercentage, .height, .bodyMass, .leanBodyMass, .basalBodyTemperature,
                                          .environmentalAudioExposure, .headphoneAudioExposure, .heartRate, .basalEnergyBurned, .activeEnergyBurned, .flightsClimbed,
                                          .vo2Max, .waistCircumference,
                                          .heartRateRecoveryOneMinute, .respiratoryRate,
                                          .bloodGlucose, .electrodermalActivity, .forcedExpiratoryVolume1, .forcedVitalCapacity, .inhalerUsage, .insulinDelivery,
                                          .numberOfTimesFallen, .peakExpiratoryFlowRate, .peripheralPerfusionIndex, .dietaryWater, .dietaryBiotin, .dietaryCaffeine,
                                          .dietaryCalcium, .dietaryCarbohydrates, .dietaryChloride, .dietaryChromium, .dietaryCopper, .dietaryEnergyConsumed,
                                          .dietaryFatMonounsaturated, .dietaryFatPolyunsaturated, .dietaryFatSaturated, .dietaryFatTotal, .dietaryFiber, .dietaryFolate,
                                          .dietaryIodine, .dietaryIron, .dietaryMagnesium, .dietaryManganese, .dietaryMolybdenum, .dietaryNiacin, .dietaryPantothenicAcid,
                                          .dietaryPhosphorus, .dietaryPotassium, .dietaryProtein, .dietaryRiboflavin, .dietarySelenium, .dietarySodium, .dietarySugar,
                                          .dietaryThiamin, .dietaryVitaminA, .dietaryVitaminB12, .dietaryVitaminB6, .dietaryVitaminC, .dietaryVitaminD, .dietaryVitaminE,
                                          .dietaryVitaminK, .dietaryZinc, .walkingSpeed, .stairAscentSpeed, .stairDescentSpeed, .walkingDoubleSupportPercentage,
                                          .sixMinuteWalkTestDistance, .uvExposure]
        for type in allTypes {
            fetchData(for: type)
        }
    }
    
    func fetchData(for type: HealthDataType) {
        var identifier: HKQuantityTypeIdentifier?
        
        switch type {
        case .stepCount: identifier = .stepCount
        case .distanceWalkingRunning: identifier = .distanceWalkingRunning
        case .distanceCycling: identifier = .distanceCycling
        case .pushCount: identifier = .pushCount
        case .distanceWheelchair: identifier = .distanceWheelchair
        case .distanceSwimming: identifier = .distanceSwimming
        case .bodyMassIndex: identifier = .bodyMassIndex
        case .bodyFatPercentage: identifier = .bodyFatPercentage
        case .height: identifier = .height
        case .bodyMass: identifier = .bodyMass
        case .leanBodyMass: identifier = .leanBodyMass
        case .basalBodyTemperature: identifier = .basalBodyTemperature
        case .environmentalAudioExposure: identifier = .environmentalAudioExposure
        case .headphoneAudioExposure: identifier = .headphoneAudioExposure
        case .heartRate: identifier = .heartRate
        case .basalEnergyBurned: identifier = .basalEnergyBurned
        case .activeEnergyBurned: identifier = .activeEnergyBurned
        case .flightsClimbed: identifier = .flightsClimbed
        case .vo2Max: identifier = .vo2Max
        case .waistCircumference: identifier = .waistCircumference
        case .heartRateRecoveryOneMinute: identifier = .heartRateVariabilitySDNN
        case .respiratoryRate: identifier = .respiratoryRate
        case .bloodGlucose: identifier = .bloodGlucose
        case .electrodermalActivity: identifier = .electrodermalActivity
        case .forcedExpiratoryVolume1: identifier = .forcedExpiratoryVolume1
        case .forcedVitalCapacity: identifier = .forcedVitalCapacity
        case .inhalerUsage: identifier = .inhalerUsage
        case .insulinDelivery: identifier = .insulinDelivery
        case .numberOfTimesFallen: identifier = .numberOfTimesFallen
        case .peakExpiratoryFlowRate: identifier = .peakExpiratoryFlowRate
        case .peripheralPerfusionIndex: identifier = .peripheralPerfusionIndex
        case .dietaryWater: identifier = .dietaryWater
        case .dietaryBiotin: identifier = .dietaryBiotin
        case .dietaryCaffeine: identifier = .dietaryCaffeine
        case .dietaryCalcium: identifier = .dietaryCalcium
        case .dietaryCarbohydrates: identifier = .dietaryCarbohydrates
        case .dietaryChloride: identifier = .dietaryChloride
        case .dietaryChromium: identifier = .dietaryChromium
        case .dietaryCopper: identifier = .dietaryCopper
        case .dietaryEnergyConsumed: identifier = .dietaryEnergyConsumed
        case .dietaryFatMonounsaturated: identifier = .dietaryFatMonounsaturated
        case .dietaryFatPolyunsaturated: identifier = .dietaryFatPolyunsaturated
        case .dietaryFatSaturated: identifier = .dietaryFatSaturated
        case .dietaryFatTotal: identifier = .dietaryFatTotal
        case .dietaryFiber: identifier = .dietaryFiber
        case .dietaryFolate: identifier = .dietaryFolate
        case .dietaryIodine: identifier = .dietaryIodine
        case .dietaryIron: identifier = .dietaryIron
        case .dietaryMagnesium: identifier = .dietaryMagnesium
        case .dietaryManganese: identifier = .dietaryManganese
        case .dietaryMolybdenum: identifier = .dietaryMolybdenum
        case .dietaryNiacin: identifier = .dietaryNiacin
        case .dietaryPantothenicAcid: identifier = .dietaryPantothenicAcid
        case .dietaryPhosphorus: identifier = .dietaryPhosphorus
        case .dietaryPotassium: identifier = .dietaryPotassium
        case .dietaryProtein: identifier = .dietaryProtein
        case .dietaryRiboflavin: identifier = .dietaryRiboflavin
        case .dietarySelenium: identifier = .dietarySelenium
        case .dietarySodium: identifier = .dietarySodium
        case .dietarySugar: identifier = .dietarySugar
        case .dietaryThiamin: identifier = .dietaryThiamin
        case .dietaryVitaminA: identifier = .dietaryVitaminA
        case .dietaryVitaminB12: identifier = .dietaryVitaminB12
        case .dietaryVitaminB6: identifier = .dietaryVitaminB6
        case .dietaryVitaminC: identifier = .dietaryVitaminC
        case .dietaryVitaminD: identifier = .dietaryVitaminD
        case .dietaryVitaminE: identifier = .dietaryVitaminE
        case .dietaryVitaminK: identifier = .dietaryVitaminK
        case .dietaryZinc: identifier = .dietaryZinc
        case .walkingSpeed: identifier = .walkingSpeed
        case .stairAscentSpeed: identifier = .stairAscentSpeed
        case .stairDescentSpeed: identifier = .stairDescentSpeed
        case .walkingDoubleSupportPercentage: identifier = .walkingDoubleSupportPercentage
        case .sixMinuteWalkTestDistance: identifier = .sixMinuteWalkTestDistance
        case .uvExposure: identifier = .uvExposure
        default: return
        }
        
        
        guard let sampleType = HKSampleType.quantityType(forIdentifier: identifier!) else {
            print("Invalid sample type")
            return
        }
        
        let query = HKSampleQuery(sampleType: sampleType, predicate: nil, limit: 0, sortDescriptors: nil) { (query, samples, error) in
            if let error = error {
                print("Error fetching data: \(error)")
                return
            }
            
            
            if let samples = samples as? [HKQuantitySample] {
                for sample in samples {
                    //                    print("\(type): \(sample.quantity.doubleValue(for: .count()))")
                    
                    let date = sample.startDate
                    var typeString: String?
                    var unitString: String?
                    var amountString: String?
                    
                    switch type {
                    case .distanceCycling:
                        typeString = "\(type)"
                        unitString = "meter"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.meter()))"
                    case .bodyFatPercentage:
                        typeString = "\(type)"
                        unitString = "percent"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.percent()))"
                    case .height:
                        typeString = "\(type)"
                        unitString = "meter"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.meter()))"
                    case .bodyMass:
                        typeString = "\(type)"
                        unitString = "kilogram"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.gramUnit(with: .kilo)))"
                    case .leanBodyMass:
                        typeString = "\(type)"
                        unitString = "kilogram"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.gramUnit(with: .kilo)))"
                    case .headphoneAudioExposure:
                        typeString = "\(type)"
                        unitString = "decibel"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.decibelAWeightedSoundPressureLevel()))"
                    case .activeEnergyBurned:
                        typeString = "\(type)"
                        unitString = "kilocalorie"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.kilocalorie()))"
                    case .waistCircumference:
                        typeString = "\(type)"
                        unitString = "meter"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.meter()))"
                    case .bloodGlucose:
                        typeString = "\(type)"
                        unitString = "mmolPerL"
                        let glucoseUnit = HKUnit.gramUnit(with: .milli).unitDivided(by: HKUnit.liter())
                        amountString = "\(sample.quantity.doubleValue(for: glucoseUnit))"
                    case .flightsClimbed:
                        typeString = "\(type)"
                        unitString = "count"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.count()))"
                    case .basalEnergyBurned:
                        typeString = "\(type)"
                        unitString = "kilocalorie"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.kilocalorie()))"
                    case .walkingDoubleSupportPercentage:
                        typeString = "\(type)"
                        unitString = "percent"
                        amountString = "\(sample.quantity.doubleValue(for: HKUnit.percent()))"
                    default:
                        continue
                    }
                    
                    if let typeString = typeString, let unitString = unitString, let amountString = amountString {
                        let dataToSave: [String: Any] = ["date": date, "type": typeString, "unit": unitString, "amount": amountString]
                        
                        let userId = "UserId"  // replace with the user's actual ID
                        db.collection("users").document(userId).collection("healthData").addDocument(data: dataToSave) { error in
                            if let error = error {
                                print("Error adding document: \(error)")
                            } else {
                                print("Document added with ID: \(userId)")
                            }
                        }
                    }
                }
            }
        }
        
        healthStore?.execute(query)
        
    }}
