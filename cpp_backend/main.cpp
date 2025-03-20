#include "cpp-httplib-master/httplib.h" // Include httplib.h
#include "json.hpp"            // Include json.hpp
#include <iostream>

#ifdef _WIN32
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
#endif

using namespace httplib;
using json = nlohmann::json;

const std::string ADDITION = "addition";
const std::string SUBTRACTION = "subtraction";
const std::string MULTIPLICATION = "multiplication";
const std::string DIVISION = "division";


int main() {
#ifdef _WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Winsock initialization failed." << std::endl;
        return 1;
    }
#endif

    Server svr;

    svr.Post("/compute", [](const Request& req, Response& res) {
        // Parse JSON from the request body
        json request_body;
        try {
            request_body = json::parse(req.body);
        } catch (const std::exception& e) {
            res.status = 400; // Bad request
            res.set_content("Invalid JSON", "text/plain");
            return;
        }

        // Extract data from JSON
        std::string title = request_body.value("title", "");
        std::string operation = request_body.value("operation", "");
        double a = request_body.value("operand_a", 0);
        double b = request_body.value("operand_b", 0);
        double resultOfComputation;

        // Perform computation
        if (operation == ADDITION) {
            resultOfComputation = a + b;
        } else if (operation == SUBTRACTION) {
            resultOfComputation = a - b;
        } else if (operation == MULTIPLICATION) {
            resultOfComputation = a * b;
        } else if (operation == DIVISION) {
            if (b == 0) {
                json response_body = {
                    {"error", "Cannot divide by zero!"}
                };
                res.set_content(response_body.dump(), "application/json");
                return;
            }
            resultOfComputation = a / b;
        }
        
        // Prepare response JSON
        json response_body = {
            {"title", title},
            {"operation", operation},
            {"result", resultOfComputation}
        };

        // Send response
        res.set_content(response_body.dump(), "application/json");
    });

    std::cout << "Server started at http://localhost:8080" << std::endl;
    svr.listen("localhost", 8080);

#ifdef _WIN32
    // Cleanup Winsock
    WSACleanup();
#endif
    return 0;
}