import { useState } from 'react';
import { createDataGenerator } from 'services/DataGenerator';

const ContactForm = ({ onSubmit, tags }) => {
  const [formData, setFormData] = useState({
    name: '',
    lastname: '',
    email: '',
    phone_main: '',
    phone_backup: '',
    tags: []
  });
  
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [Generator] = useState(() => createDataGenerator());

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) return 'Email is required';
    if (!emailRegex.test(email)) return 'Please enter a valid email address';
    return '';
  };

  const validateField = (name, value) => {
    let error = '';
    
    switch (name) {
      case 'name':
        if (!value.trim()) error = 'First name is required';
        break;
      case 'lastname':
        if (!value.trim()) error = 'Last name is required';
        break;
      case 'email':
        error = validateEmail(value);
        break;
      case 'phone_main':
        if (!value.trim()) error = 'Phone is required';
        break;
      default:
        break;
    }
    
    return error;
  };

  const generateRandomData = () => {
    const newContact = Generator.createContact(tags);
    setFormData(newContact);
    setErrors({}); // Clear any existing errors
  };

  const resetForm = () => {
    setFormData({
      name: '',
      lastname: '',
      email: '',
      phone_main: '',
      phone_backup: '',
      tags: []
    });
    setErrors({});
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
        
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Real-time validation for email and phone
    if (name === 'email' || name === 'phone_main') {
      const error = validateField(name, value);
      if (error) {
        setErrors(prev => ({
          ...prev,
          [name]: error
        }));
      }
    }
  };

  const handleTagsChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions);
    const selectedTags = selectedOptions.map(option => option.value);
    setFormData(prev => ({
      ...prev,
      tags: selectedTags
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Validate all required fields
    Object.keys(formData).forEach(key => {
      if (key !== 'tags' && key !== 'phone_backup') {
        const error = validateField(key, formData[key]);
        if (error) {
          newErrors[key] = error;
        }
      }
    });

    // Validate phone_backup if provided
    if (formData.phone_backup) {
      const error = validateField('phone_backup', formData.phone_backup);
      if (error) {
        newErrors.phone_backup = error;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      await onSubmit(formData);
      setFormData({
        name: '',
        lastname: '',
        email: '',
        phone_main: '',
        phone_backup: '',
        tags: []
      });
      setErrors({});
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('Failed to create contact. Please check your input and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getInputClassName = (fieldName) => {
    const baseClasses = "w-full px-3 py-2 border rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent transition-colors";
    const errorClasses = errors[fieldName] 
      ? "border-red-500 dark:border-red-400 focus:ring-red-500 dark:focus:ring-red-400" 
      : "border-gray-300 dark:border-gray-600 focus:ring-blue-500 dark:focus:ring-blue-400";
    return `${baseClasses} ${errorClasses}`;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-600">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Add New Contact</h2>
      
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              First Name *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className={getInputClassName('name')}
              placeholder="Enter first name"
            />
            {errors.name && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.name}</p>}
          </div>
          
          <div>
            <label htmlFor="lastname" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Last Name *
            </label>
            <input
              type="text"
              id="lastname"
              name="lastname"
              value={formData.lastname}
              onChange={handleChange}
              required
              className={getInputClassName('lastname')}
              placeholder="Enter last name"
            />
            {errors.lastname && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.lastname}</p>}
          </div>
        </div>
        
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Email *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className={getInputClassName('email')}
            placeholder="Enter email address"
          />
          {errors.email && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.email}</p>}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="phone_main" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Main Phone *
            </label>
            <input
              type="tel"
              id="phone_main"
              name="phone_main"
              value={formData.phone_main}
              onChange={handleChange}
              required
              className={getInputClassName('phone_main')}
              placeholder="Enter main phone"
            />
            {errors.phone_main && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.phone_main}</p>}
          </div>
          
          <div>
            <label htmlFor="phone_backup" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Backup Phone
            </label>
            <input
              type="tel"
              id="phone_backup"
              name="phone_backup"
              value={formData.phone_backup}
              onChange={handleChange}
              className={getInputClassName('phone_backup')}
              placeholder="Enter backup phone (optional)"
            />
            {errors.phone_backup && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.phone_backup}</p>}
          </div>
        </div>
        
        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Tags
          </label>
          <select
            id="tags"
            name="tags"
            multiple
            value={formData.tags.map(String)}
            onChange={handleTagsChange}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent h-24"
          >
            {tags.map(tag => (
              <option key={tag.id} value={tag.id} className="bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                {tag.label}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Hold Ctrl/Cmd to select multiple tags</p>
        </div>
        
        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || Object.keys(errors).some(key => errors[key])}
            className="flex-1 bg-blue-600 dark:bg-blue-700 text-white py-2 px-4 rounded-md hover:bg-blue-700 dark:hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:ring-offset-2 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? 'Creating...' : 'Create Contact'}
          </button>
          
          <button
            type="button"
            onClick={generateRandomData}
            disabled={isSubmitting}
            className="flex-1 sm:flex-initial bg-green-600 dark:bg-green-700 text-white py-2 px-4 rounded-md hover:bg-green-700 dark:hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-500 dark:focus:ring-green-400 focus:ring-offset-2 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Generate Random
          </button>
          
          <button
            type="button"
            onClick={resetForm}
            disabled={isSubmitting}
            className="flex-1 sm:flex-initial bg-gray-600 dark:bg-gray-700 text-white py-2 px-4 rounded-md hover:bg-gray-700 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 dark:focus:ring-gray-400 focus:ring-offset-2 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContactForm;