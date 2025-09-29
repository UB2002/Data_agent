export default function Message({ role, content }) {
  return (
    <div
      className={`p-3 my-2 rounded-xl max-w-lg ${
        role === "user" ? "bg-blue-100 ml-auto" : "bg-gray-100"
      }`}
    >
      <p className="text-sm">{content}</p>
    </div>
  );
}
