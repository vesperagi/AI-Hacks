import Foundation

class Chatbot {
    
    func getBotResponse(for userInput: String, completion: @escaping (String) -> Void) {
        guard let url = URL(string: "https://light-reality-293618.uc.r.appspot.com/api/chat_input") else {
            print("Invalid URL")
            completion("Error: Invalid URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        
        let postData = "input=\(userInput)".data(using: .utf8)
        request.httpBody = postData
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                print("Network request error: \(error)")
                completion("Something went wrong!")
            }
            if let data = data {
                do {
                    if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
                        print("Received JSON response: \(jsonResponse)")
                        if let responseText = jsonResponse["response"] as? String {
                            completion(responseText)
                        } else {
                            completion("Sorry, I couldn't process your request.")
                        }
                    }
                } catch {
                    print("JSON parsing error: \(error)")
                    if let jsonString = String(data: data, encoding: .utf8) {
                        print("Received JSON string: \(jsonString)")
                    }
                    completion("Something went wrong!")
                }
            }
        }

        task.resume()
    }
}
