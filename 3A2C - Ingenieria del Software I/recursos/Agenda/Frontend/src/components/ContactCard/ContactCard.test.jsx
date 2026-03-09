import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import ContactCard from './ContactCard';

// Mock window.confirm
const mockConfirm = vi.fn();
Object.defineProperty(window, 'confirm', {
  value: mockConfirm,
  writable: true
});

// Mock window.alert
const mockAlert = vi.fn();
Object.defineProperty(window, 'alert', {
  value: mockAlert,
  writable: true
});

describe('ContactCard', () => {
  const mockOnDelete = vi.fn();

  const mockContact = {
    id: 1,
    name: 'John',
    lastname: 'Doe',
    email: 'john.doe@example.com',
    phone_main: '+1234567890',
    phone_backup: '+0987654321',
    tags: [
      { id: 1, label: 'Work' },
      { id: 2, label: 'Family' }
    ]
  };

  const mockContactWithoutBackupPhone = {
    id: 2,
    name: 'Jane',
    lastname: 'Smith',
    email: 'jane.smith@example.com',
    phone_main: '+1122334455',
    phone_backup: '',
    tags: [{ id: 3, label: 'Friends' }]
  };

  const mockContactWithoutTags = {
    id: 3,
    name: 'Bob',
    lastname: 'Johnson',
    email: 'bob.johnson@example.com',
    phone_main: '+5566778899',
    phone_backup: '',
    tags: []
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Default State', () => {
    it('renders contact information correctly', () => {
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
      expect(screen.getByText('+1234567890')).toBeInTheDocument();
      expect(screen.getByText('+0987654321')).toBeInTheDocument();
    });

    it('renders contact without backup phone correctly', () => {
      render(
        <ContactCard
          contact={mockContactWithoutBackupPhone}
          onDelete={mockOnDelete}
        />
      );

      expect(screen.getByText('Jane Smith')).toBeInTheDocument();
      expect(screen.getByText('+1122334455')).toBeInTheDocument();
      
      // Backup phone should not be displayed
      expect(screen.queryByText('+0987654321')).not.toBeInTheDocument();
    });

    it('renders contact without tags correctly', () => {
      render(
        <ContactCard
          contact={mockContactWithoutTags}
          onDelete={mockOnDelete}
        />
      );

      expect(screen.getByText('Bob Johnson')).toBeInTheDocument();
      
      // No tags should be displayed
      expect(screen.queryByText('Work')).not.toBeInTheDocument();
      expect(screen.queryByText('Family')).not.toBeInTheDocument();
      expect(screen.queryByText('Friend')).not.toBeInTheDocument();
    });
  });

  describe('Data Exceptions', () => {
    it('handles empty contact name gracefully', () => {
      const contactWithEmptyName = {
        ...mockContact,
        name: '',
        lastname: ''
      };

      render(
        <ContactCard
          contact={contactWithEmptyName}
          onDelete={mockOnDelete}
        />
      );

      // Should still render without crashing
      expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
    });

    it('handles missing contact properties', () => {
      const incompleteContact = {
        id: 4,
        name: 'Test',
        lastname: 'User',
        // Missing phone_main and email
      };

      expect(() => {
        render(
          <ContactCard
            contact={incompleteContact}
            onDelete={mockOnDelete}
          />
        );
      }).not.toThrow();
    });
  });

  describe('UI Elements and Icons', () => {
    it('displays all required icons', () => {
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      // Check for user icon (in the name section)
      const userIcon = screen.getByTestId('user-icon');
      expect(userIcon).toBeTruthy();

      // Check for email icon
      const emailIcon = screen.getByTestId('mail-icon');
      expect(emailIcon).toBeTruthy();

      // Check for phone icons
      const phoneIcons = screen.getAllByTestId('phone-icon');
      expect(phoneIcons.length).toBeGreaterThan(0);

      // Check for delete icon
      const deleteIcon = screen.getByTestId('trash-icon');
      expect(deleteIcon).toBeTruthy();
    });

    it('applies correct CSS classes for styling', () => {
      const { container } = render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const card = container.firstChild;
      expect(card).toHaveClass('bg-white', 'rounded-lg', 'shadow-md');
    });

    it('applies hover effects on delete button', () => {
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      expect(deleteButton).toHaveClass('hover:text-red-700', 'transition-colors');
    });
  });

  describe('Tags', () => {
    it('displays correct tags for contact', () => {
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      // Should display tags with Ids 1 and 2
      expect(screen.getByText('Work')).toBeInTheDocument();
      expect(screen.getByText('Family')).toBeInTheDocument();
      
      // Should not display tag with id 3
      expect(screen.queryByText('Friend')).not.toBeInTheDocument();
    });

    it('does not display tags section when contact has no tags', () => {
      render(
        <ContactCard
          contact={mockContactWithoutTags}
          onDelete={mockOnDelete}
        />
      );

      const tagIcon = screen.queryByTestId('tag-icon');
      expect(tagIcon).not.toBeInTheDocument();
    });
  });

  describe('Delete contact', () => {
    it('renders delete button', () => {
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      expect(deleteButton).toBeInTheDocument();
    });

    it('shows confirmation dialog when delete button is clicked', async () => {
      mockConfirm.mockReturnValue(true);
      
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      await userEvent.click(deleteButton);

      expect(mockConfirm).toHaveBeenCalledWith('Are you sure you want to delete this contact?');
    });

    it('calls onDelete when user confirms deletion', async () => {
      mockConfirm.mockReturnValue(true);
      mockOnDelete.mockResolvedValue();
      
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      await userEvent.click(deleteButton);

      expect(mockOnDelete).toHaveBeenCalledWith(1);
    });

    it('does not call onDelete when user cancels deletion', async () => {
      mockConfirm.mockReturnValue(false);
      
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      await userEvent.click(deleteButton);

      expect(mockOnDelete).not.toHaveBeenCalled();
    });

    it('shows error alert when delete fails', async () => {
      mockConfirm.mockReturnValue(true);
      mockOnDelete.mockRejectedValue(new Error('Delete failed'));
      
      render(
        <ContactCard
          contact={mockContact}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /delete contact/i });
      await userEvent.click(deleteButton);

      await waitFor(() => {
        expect(mockAlert).toHaveBeenCalledWith('Failed to delete contact. Please try again.');
      });
    });
  });

});