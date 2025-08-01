import React, { useState, useEffect } from "react";
import { 
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger 
} from "../components/ui/accordion";
import { Badge } from "../components/ui/badge";
import { publicAPI } from "../services/api";
import { mockData } from "../utils/mockData";

const FAQ = () => {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFAQs = async () => {
      try {
        const response = await publicAPI.getFAQs();
        setFaqs(response.data);
      } catch (error) {
        console.error("Failed to fetch FAQs:", error);
        // Fallback to mock data
        setFaqs(mockData.faqs);
      } finally {
        setLoading(false);
      }
    };

    fetchFAQs();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-slate-800 text-purple-300 border-purple-500/30">
            FAQ
          </Badge>
          <h1 className="text-4xl sm:text-6xl font-bold mb-6">
            Frequently Asked{" "}
            <span className="bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              Questions
            </span>
          </h1>
          <p className="text-xl text-gray-300">
            Find answers to common questions about Blotato and how it can help you scale your content creation.
          </p>
        </div>

        {/* FAQ Accordion */}
        {loading ? (
          <div className="text-center text-gray-400">Loading FAQs...</div>
        ) : (
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem 
                key={faq.id || index} 
                value={`item-${index}`}
                className="bg-slate-900 border-slate-700 rounded-lg px-6"
              >
                <AccordionTrigger className="text-white hover:text-purple-300 text-left py-6">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-gray-300 pb-6">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}

        {/* Contact Support */}
        <div className="text-center mt-16 p-8 bg-slate-900 rounded-2xl border border-slate-700">
          <h2 className="text-2xl font-bold text-white mb-4">
            Still have questions?
          </h2>
          <p className="text-gray-300 mb-6">
            Our support team is here to help you get the most out of Blotato.
          </p>
          <button className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-3 rounded-xl font-semibold transform hover:scale-105 transition-all duration-200">
            Contact Support
          </button>
        </div>
      </div>
    </div>
  );
};

export default FAQ;