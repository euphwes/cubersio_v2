export const load = async ({ fetch }) => {
  const response = await fetch('/api/');
  const responseData = await response.json();

  return {
    events: responseData.events
  };
};
