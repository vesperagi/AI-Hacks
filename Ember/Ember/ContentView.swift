import SwiftUI

struct EmberButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(minWidth: 0, maxWidth: .infinity)
            .frame(height: 50)
            .foregroundColor(.white)
            .font(.system(size: 18, weight: .semibold, design: .rounded))
            .padding(.vertical)
            .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .leading, endPoint: .trailing))
            .cornerRadius(10)
            .padding(.horizontal)
    }
}

struct ContentView: View {
    @ObservedObject private var healthKitViewModel = HealthKitViewModel()

    // Rotating text data
    @State private var currentIndex = 0
    let rotatingTexts = ["Your Health Companion", "Data Driven Health", "Talk to Your Health Assistant"]

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Spacer()
                Image("localhost_3000_home_2_1_2")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 200, height: 200)
                Text("Ember")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(Color.blue)
                Text(rotatingTexts[currentIndex])
                    .font(.headline)
                    .foregroundColor(Color.gray)
                    .animation(.easeInOut(duration: 1.0))
                    .onAppear {
                        
                        Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { _ in
                            currentIndex = (currentIndex + 1) % rotatingTexts.count
                        }
                    }
                Spacer()
                NavigationLink(destination: ChatView(initialPrompt: "Give me tips to improve my overall health and build more muscle?")) {
                    Text("Ask Ember")
                }
                .buttonStyle(EmberButtonStyle())
                NavigationLink(destination: ChatView(initialPrompt: "What was my health data like on February 02?")) {
                    Text("Doctors Notes")
                }
                .buttonStyle(EmberButtonStyle())
                Button(action: {
                    healthKitViewModel.requestAuthorization()
                    healthKitViewModel.fetchAllData()
                }) {
                    Text("Fetch Data")
                }
                .buttonStyle(EmberButtonStyle())
                Spacer()
            }
        }
        .padding()
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
