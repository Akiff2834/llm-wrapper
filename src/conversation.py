"""
Conversation Manager - Handles chat history and message management
"""

from typing import List, Dict
from datetime import datetime


class ConversationManager:
    """
    Manages conversation history for the LLM chat interface
    Stores messages with roles: user, assistant, function
    """
    
    def __init__(self):
        """Initialize conversation manager with empty history"""
        self.messages: List[Dict[str, str]] = []
        self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str):
        """
        Add a message to conversation history
        
        Args:
            role: Message role ('user', 'assistant', or 'function')
            content: Message content
        """
        if role not in ["user", "assistant", "function"]:
            raise ValueError(f"Invalid role: {role}. Must be 'user', 'assistant', or 'function'")
        
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get all messages in conversation
        
        Returns:
            List of message dictionaries
        """
        return self.messages
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """
        Get last N messages
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of last N messages
        """
        return self.messages[-n:] if n > 0 else []
    
    def clear(self):
        """Clear all conversation history"""
        self.messages = []
        self.created_at = datetime.now()
    
    def get_conversation_summary(self) -> Dict[str, any]:
        """
        Get summary statistics about the conversation
        
        Returns:
            Dictionary with conversation metadata
        """
        user_messages = sum(1 for msg in self.messages if msg["role"] == "user")
        assistant_messages = sum(1 for msg in self.messages if msg["role"] == "assistant")
        function_calls = sum(1 for msg in self.messages if msg["role"] == "function")
        
        return {
            "total_messages": len(self.messages),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "function_calls": function_calls,
            "created_at": self.created_at.isoformat()
        }
