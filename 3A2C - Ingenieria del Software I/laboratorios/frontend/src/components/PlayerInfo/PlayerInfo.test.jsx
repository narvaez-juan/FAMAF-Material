import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlayerInfo from './PlayerInfo';

describe('PlayerInfo', () => {
  it('renders the player name', () => {
    render(<PlayerInfo jugador={{ id_jugador: 1, nombre: 'Pedro' }} esTurnoActual={false} />);
    expect(screen.getByText('Pedro')).toBeInTheDocument();
  });

  it('truncates the name manually if it is too long', () => {
    const longName = 'ThisLongNameShouldNotBreakTheLayout';
    const expected = longName.slice(0, 17) + '...';
    render(<PlayerInfo jugador={{ id_jugador: 2, nombre: longName }} esTurnoActual={false} />);
    expect(screen.getByText(expected)).toBeInTheDocument();
    expect(screen.queryByText(longName)).not.toBeInTheDocument();
  });

  it('applies highlight style when it is the current turn', () => {
    render(<PlayerInfo jugador={{ id_jugador: 3, nombre: 'María' }} esTurnoActual={true} />);
    const el = screen.getByText('María').closest('div');
    expect(el.className).toMatch(/border-yellow-300/);
    expect(el.className).toMatch(/bg-gradient-to-br/);
  });

  it('does not apply highlight style when it is not the current turn', () => {
    render(<PlayerInfo jugador={{ id_jugador: 4, nombre: 'Juan' }} esTurnoActual={false} />);
    const el = screen.getByText('Juan').closest('div');
    expect(el.className).toMatch(/border-slate-700/);
    expect(el.className).not.toMatch(/border-yellow-300/);
  });
});
