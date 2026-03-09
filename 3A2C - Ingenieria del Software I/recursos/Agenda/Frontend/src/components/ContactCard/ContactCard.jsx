import { Trash2, User, Mail, Phone, Tag } from 'lucide-react';
//import styles from './ContactCard.module.css';

const ContactCard = ({
  contact,
  onDelete,
}) => {

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this contact?')) {
      try {
        await onDelete(contact.id);
      } catch (error) {
        alert('Failed to delete contact. Please try again.');
      }
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-600 hover:shadow-lg dark:hover:shadow-xl transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-2">
          <User className="w-5 h-5 text-gray-600 dark:text-gray-400" data-testid="user-icon"/>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {contact.name} {contact.lastname}
          </h3>
        </div>
        <button
          onClick={handleDelete}
          className="text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20"
          title="Delete contact"
        >
          <Trash2 className="w-5 h-5" data-testid="trash-icon"/>
        </button>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center space-x-2">
          <Mail className="w-4 h-4 text-gray-500 dark:text-gray-400" data-testid="mail-icon"/>
          <span className="text-gray-700 dark:text-gray-300">{contact.email}</span>
        </div>
        
        <div className="flex items-center space-x-2">
          <Phone className="w-4 h-4 text-gray-500 dark:text-gray-400" data-testid="phone-icon"/>
          <span className="text-gray-700 dark:text-gray-300">{contact.phone_main}</span>
        </div>
        
        {contact.phone_backup && (
          <div className="flex items-center space-x-2">
            <Phone className="w-4 h-4 text-gray-400 dark:text-gray-500" data-testid="phone-icon"/>
            <span className="text-gray-600 dark:text-gray-400 text-sm">{contact.phone_backup}</span>
          </div>
        )}
        
        {contact.tags?.length > 0 && (
          <div className="flex items-center space-x-2 mt-3">
            <Tag className="w-4 h-4 text-gray-500 dark:text-gray-400" />
            <div className="flex flex-wrap gap-1">
              {contact.tags.map(tag => (
                <span
                  key={tag.id}
                  className="inline-block bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 text-xs px-2 py-1 rounded-full border border-blue-200 dark:border-blue-700/50"
                >
                  {tag.label}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContactCard;