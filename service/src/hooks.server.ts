import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ resolve, event }) => {
  const response = await resolve(event);

  response.headers.append('Access-Control-Allow-Origin', "*");
  return response;
};
