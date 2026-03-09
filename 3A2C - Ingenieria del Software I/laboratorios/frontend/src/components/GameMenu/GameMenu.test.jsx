import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import GameMenu from './GameMenu';

const mockNavigate = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('GameMenu', () => {

    describe('Default state', () => {
        it('renders create game and join game buttons', () => {
            render(<GameMenu createGameLink="/games/create" listGamesLink="/games/list" />);

            expect(screen.getByRole('button', { name: /Create Game/i })).toBeInTheDocument();
            expect(screen.getByRole('button', { name: /Join Game/i })).toBeInTheDocument();
        });
    
        it('renders title and description text', () => {
            render(<GameMenu createGameLink="/games/create" listGamesLink="/games/list" />);

            expect(screen.getByText(/Agatha Christie's/i)).toBeInTheDocument();
            expect(screen.getByRole('heading', { level: 2, name: /Death on the Cards/i })).toBeInTheDocument();
            expect(screen.getByText(/A game of suspicions, secrets... and a bit of betrayal./i)).toBeInTheDocument();
        });
    
    });

    describe('Button navigation', () => {
        it('navigates to create game page when Create Game button is clicked', async () => {
            render(<GameMenu createGameLink="/games/create" listGamesLink="/games/list" />);

            await userEvent.click(screen.getByRole('button', { name: /Create Game/i }));

            await waitFor(() => {
                expect(mockNavigate).toHaveBeenCalledWith("/games/create");
            });
        });

        it('navigates to game list page when Join Game button is clicked', async () => {
            render(<GameMenu createGameLink="/games/create" listGamesLink="/games/list" />);

            fireEvent.click(screen.getByRole('button', { name: /Join Game/i }));
            await waitFor(() => {
                expect(mockNavigate).toHaveBeenCalledWith("/games/list");
            });
        });
    });
});