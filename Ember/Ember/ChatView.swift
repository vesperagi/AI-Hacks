import SwiftUI

struct Message: Identifiable, Hashable {
    let id = UUID()
    let content: String
    let isFromUser: Bool
}

struct TypingView: View {
    @State private var showDot = 0

    let timer = Timer.publish(every: 0.5, on: .main, in: .common).autoconnect()

    var body: some View {
        HStack {
            Spacer()
            Text("...\(String(repeating: ".", count: showDot))")
                .onReceive(timer) { _ in
                    withAnimation {
                        self.showDot = (self.showDot + 1) % 4
                    }
                }
                .padding(10)
                .background(Color.gray)
                .foregroundColor(.white)
                .cornerRadius(10)
        }
    }
}

struct ChatView: View {
    @State private var userInput = ""
    @State private var messages = [Message]()
    @State private var isTyping = false
    private var chatbot = Chatbot()
    var initialPrompt: String?

    init(initialPrompt: String? = nil) {
        self.initialPrompt = initialPrompt
    }


    var body: some View {
        VStack {
            ScrollViewReader { scrollView in
                ScrollView {
                    ForEach(messages, id: \.self) { message in
                        HStack {
                            if message.isFromUser {
                                Spacer()
                            }
                            Text(message.content)
                                .padding(10)
                                .background(message.isFromUser ? Color.blue : Color.gray)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                            if !message.isFromUser {
                                Spacer()
                            }
                        }
                    }
                    .onChange(of: messages) { _ in
                        DispatchQueue.main.async {
                            withAnimation {
                                scrollView.scrollTo(messages.last, anchor: .bottom)
                            }
                        }
                    }
                    if isTyping {
                        TypingView()
                    }
                }
            }

            HStack {
                TextField("Type something...", text: $userInput)
                    .padding(10)
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                    .padding(.horizontal)

                Button(action: {
                    processUserInput(userInput)
                }) {
                    Image(systemName: "paperplane.fill")
                        .resizable()
                        .frame(width: 25, height: 20)
                        .padding()
                }
                .background(Color.blue)
                .cornerRadius(50)
                .foregroundColor(.white)
                .padding(.trailing)
            }
        }
        .padding()
        .onAppear {
            if let prompt = initialPrompt {
                processUserInput(prompt)
            }
        }
    }

    func processUserInput(_ input: String) {
        isTyping = true
        let message = Message(content: input, isFromUser: true)
        messages.append(message)
        userInput = ""
        chatbot.getBotResponse(for: message.content) { (response) in
            DispatchQueue.main.async {
                isTyping = false
                let botMessage = Message(content: response, isFromUser: false)
                messages.append(botMessage)
            }
        }
    }
}

struct ChatView_Previews: PreviewProvider {
    static var previews: some View {
        ChatView()
    }
}
