const { send } = useRosterSocket(companyId, (data) => {
  setRoster((prev) => {
    const updated = { ...prev }
    updated[data.staffId][data.date] = data.shift
    return updated
  })
})

const handleShiftChange = (staffId, date, shift) => {
  send({
    staffId,
    date,
    shift,
  })
}