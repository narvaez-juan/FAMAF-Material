import { createHttpService } from '../../services/HTTPServices';

export default async function fetchPlayerInfo(gameId) {
  const httpService = createHttpService();

  try {
    const turnInfo = await httpService.getTurnInfo(gameId);
    const { jugadores, turnoActual, enCurso } = turnInfo;
    return { jugadores, turnoActual, enCurso };
  } catch (error) {
    console.error('Error getting turn information:', error);
    throw error;
  }
}
