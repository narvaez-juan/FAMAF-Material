import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest' 
import JoinGame from './JoinGame'
import { beforeEach } from "vitest";
import { useParams, useNavigate } from 'react-router-dom'

vi.mock('react-router-dom' , () => ({
    useParams: vi.fn(),
    useNavigate: vi.fn(),
}))

describe('JoinGame Component', () => {
    const mockNavigate = vi.fn()
    beforeEach(() => {
        useNavigate.mockReturnValue(mockNavigate)
    })


    it('Must render correctly and show the game ID from the URL', () => {
        //NOTE - Simulates the URL with Id
        useParams.mockReturnValue({gameId: '52'})


        //NOTE - Render the component
        render(<JoinGame/>)

        //NOTE - We check if the Id was/is render
        expect(screen.getByText(/Join Existing Game - ID: 52/)).toBeInTheDocument()
        const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});

    })




    it('must navigate to the lobby on successful form submission', async () => {
        useParams.mockReturnValue({ gameId: '1' })

        global.fetch = vi.fn()
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ player_id: 5, name: 'Test Player' }),
        })  

        render(<JoinGame />)

        await userEvent.type(screen.getByLabelText(/Player Name/i), 'Joe Mama')
        await userEvent.type(screen.getByLabelText(/Birth Date/i), '2000-01-01')
        await userEvent.click(screen.getByRole('button', { name: /Submit/i }))

        await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/games/1/lobbies', {
            state: { playerId: 5 },
        });
        });
    })
})