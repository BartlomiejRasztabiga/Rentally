const cleanupFalsyFields = object => {
  // if field is falsy (empty string, null, undefined), set it to null
  Object.entries(object).forEach((entry) => {
    let key, value;
    [key, value] = entry;
    if (!value) {
      object[key] = null;
    }
  });
  return object;
};

export default cleanupFalsyFields;
