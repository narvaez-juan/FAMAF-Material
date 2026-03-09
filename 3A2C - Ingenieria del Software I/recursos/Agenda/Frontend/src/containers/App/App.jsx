import { useEffect, useState } from 'react';
import AppLayout from './components/AppLayout';

import { createHttpService } from 'services/HttpService';
import { createWSService } from 'services/WSService';

const App = () => {
  const [contacts, setContacts] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [httpService] = useState(() => createHttpService());
  const [wsService] = useState(() => createWSService());

  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        
        // Load tags and contacts
        const [tagsData, contactsData] = await Promise.all([
          httpService.getTags().catch(() => []), // Fallback to empty array if tags endpoint fails
          httpService.getContacts().catch(() => []) // Fallback to empty array if contacts endpoint fails
        ]);

        setTags(tagsData);
        setContacts(contactsData);
        
        // Initialize WebSocket
        if (wsService.isConnected) {
          console.warn('WebSocket is already connected. Reusing existing connection.');
        } else {
          wsService.connect();
          wsService.on('contactAdd', (newContact) => {
            setContacts(prev => {
              const exists = prev.some(contact => contact.id === newContact.id);
              return exists ? prev : [...prev, newContact];
            });
          });
          
          wsService.on('contactRemove', (deletedContactId) => {
            setContacts(prev => prev.filter(contact => contact.id !== deletedContactId));
          });
        }
        
      } catch (error) {
        console.error('Failed to initialize app:', error);
      } finally {
        setLoading(false);
      }
    };

    init();

    // Cleanup WebSocket on unmount
    return () => {
      wsService.disconnect();
    };
  }, [httpService, wsService]);

  const handleCreateContact = async (contactData) => {
    try {
      const response = await httpService.createContact(contactData);

      // The new contact will be added via WebSocket, but as fallback:
      const newContact = await httpService.getContact(response.id);
      
      // Check if contact already exists (WebSocket might have added it)
      setContacts(prev => {
        const exists = prev.some(contact => contact.id === newContact.id);
        return exists ? prev : [...prev, newContact];
      });
    } catch (error) {
      console.error('Failed to create contact:', error);
      throw error;
    }
  };

  const handleDeleteContact = async (contactId) => {
    try {
      await httpService.deleteContact(contactId);

      // Remove from local state (WebSocket will also trigger this)
      setContacts(prev => prev.filter(contact => contact.id !== contactId));
    } catch (error) {
      console.error('Failed to delete contact:', error);
      throw error;
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout
      contacts={contacts}
      onCreateContact={handleCreateContact}
      onRemoveContact={handleDeleteContact}
      tags={tags}
    />
  );
};

export default App;
