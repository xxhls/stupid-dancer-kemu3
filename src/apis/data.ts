import service from "../utils/request";

export async function getData(): Promise<{
    total: number,
    row: number,
    col: number
}> {
     return (await service.get("/data")).data;
}

export async function getDataByIndex(index: number): Promise<number[][]> {
    return (await service.get(`/data/${index}`)).data;
}
